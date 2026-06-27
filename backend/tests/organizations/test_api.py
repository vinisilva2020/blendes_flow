from rest_framework import status
from rest_framework.test import APITestCase

from apps.organizations.models import Organization
from tests.authentication.factories import create_user, issue_access_token_for_user
from tests.organizations.factories import create_organization


ORGANIZATION_LIST_URL = "/api/v1/organizations/"


def organization_detail_url(organization_id):
    return f"/api/v1/organizations/{organization_id}/"


class OrganizationsAPITests(APITestCase):
    def authenticate(self, user):
        token = issue_access_token_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_requires_authentication(self):
        response = self.client.get(ORGANIZATION_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"]["code"], "authentication_required")

    def test_list_returns_only_current_user_active_organizations(self):
        user = create_user(username="api-list-user")
        other_user = create_user(username="api-list-other")
        active_org = create_organization(
            created_by=user,
            name="Active Org",
        )
        create_organization(
            created_by=user,
            name="Inactive Org",
            is_active=False,
        )
        create_organization(
            created_by=other_user,
            name="Other Org",
        )

        self.authenticate(user)
        response = self.client.get(ORGANIZATION_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], active_org.id)
        self.assertEqual(response.data[0]["name"], "Active Org")

    def test_create_organization_sets_current_user_as_owner(self):
        user = create_user(username="api-create-user")
        self.authenticate(user)

        response = self.client.post(
            ORGANIZATION_LIST_URL,
            {
                "name": "Created API Org",
                "description": "Created through API",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        organization = Organization.objects.get(id=response.data["id"])
        self.assertEqual(organization.created_by, user)

    def test_create_duplicate_organization_returns_conflict(self):
        user = create_user(username="api-create-duplicate")
        create_organization(name="Duplicate API Org")
        self.authenticate(user)

        response = self.client.post(
            ORGANIZATION_LIST_URL,
            {"name": "Duplicate API Org"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["error"]["code"], "organization_already_exists")

    def test_retrieve_organization_for_owner(self):
        user = create_user(username="api-detail-owner")
        organization = create_organization(created_by=user)
        self.authenticate(user)

        response = self.client.get(
            organization_detail_url(organization.id),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], organization.id)

    def test_retrieve_organization_returns_not_found_for_other_user(self):
        user = create_user(username="api-detail-outsider")
        organization = create_organization()
        self.authenticate(user)

        response = self.client.get(
            organization_detail_url(organization.id),
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["error"]["code"],
            "organization_not_found",
        )

    def test_owner_can_patch_organization(self):
        user = create_user(username="api-patch-owner")
        organization = create_organization(created_by=user, name="Before Patch")
        self.authenticate(user)

        response = self.client.patch(
            organization_detail_url(organization.id),
            {"name": "After Patch"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        organization.refresh_from_db()
        self.assertEqual(organization.name, "After Patch")

    def test_other_user_cannot_patch_organization(self):
        user = create_user(username="api-patch-outsider")
        organization = create_organization(name="Patch Hidden")
        self.authenticate(user)

        response = self.client.patch(
            organization_detail_url(organization.id),
            {"name": "Forbidden Update"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_delete_organization(self):
        user = create_user(username="api-delete-owner")
        organization = create_organization(created_by=user)
        self.authenticate(user)

        response = self.client.delete(
            organization_detail_url(organization.id),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Organization.objects.filter(id=organization.id).exists())

    def test_other_user_cannot_delete_organization(self):
        user = create_user(username="api-delete-outsider")
        organization = create_organization(name="Delete Hidden")
        self.authenticate(user)

        response = self.client.delete(
            organization_detail_url(organization.id),
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Organization.objects.filter(id=organization.id).exists())
