from rest_framework import status
from rest_framework.test import APITestCase

from apps.organizations.models import Organization, OrganizationMembership, Role
from tests.authentication.factories import create_user, issue_access_token_for_user
from tests.organizations.factories import (
    create_membership,
    create_organization,
    create_organization_with_membership,
)


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
        active_org, _ = create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
            name="Active Org",
        )
        create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
            name="Inactive Org",
            is_active=False,
        )
        create_organization_with_membership(
            user=other_user,
            role=Role.MEMBER,
            name="Other Org",
        )

        self.authenticate(user)
        response = self.client.get(ORGANIZATION_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], active_org.id)
        self.assertEqual(response.data[0]["name"], "Active Org")

    def test_create_organization_creates_owner_membership(self):
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
        self.assertTrue(
            OrganizationMembership.objects.filter(
                user=user,
                organization=organization,
                role=Role.OWNER,
            ).exists()
        )

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

    def test_retrieve_organization_for_member(self):
        user = create_user(username="api-detail-member")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
        )
        self.authenticate(user)

        response = self.client.get(
            organization_detail_url(organization.id),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], organization.id)

    def test_retrieve_organization_returns_not_found_for_non_member(self):
        user = create_user(username="api-detail-outsider")
        organization = create_organization()
        self.authenticate(user)

        response = self.client.get(
            organization_detail_url(organization.id),
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["error"]["code"],
            "user_not_member_of_organization",
        )

    def test_member_cannot_patch_organization(self):
        user = create_user(username="api-patch-member")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
        )
        self.authenticate(user)

        response = self.client.patch(
            organization_detail_url(organization.id),
            {"name": "Member Update"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["error"]["code"], "permission_denied")

    def test_admin_can_patch_organization(self):
        owner = create_user(username="api-patch-owner")
        admin = create_user(username="api-patch-admin")
        organization = create_organization(created_by=owner, name="Before Patch")
        create_membership(user=admin, organization=organization, role=Role.ADMIN)
        self.authenticate(admin)

        response = self.client.patch(
            organization_detail_url(organization.id),
            {"name": "After Patch"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        organization.refresh_from_db()
        self.assertEqual(organization.name, "After Patch")

    def test_owner_can_delete_organization(self):
        user = create_user(username="api-delete-owner")
        organization, _ = create_organization_with_membership(user=user)
        self.authenticate(user)

        response = self.client.delete(
            organization_detail_url(organization.id),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Organization.objects.filter(id=organization.id).exists())

    def test_member_cannot_delete_organization(self):
        user = create_user(username="api-delete-member")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
        )
        self.authenticate(user)

        response = self.client.delete(
            organization_detail_url(organization.id),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["error"]["code"], "permission_denied")
        self.assertTrue(Organization.objects.filter(id=organization.id).exists())
