from rest_framework import status
from rest_framework.test import APITestCase

from apps.blendes.models.execution import Blave, BlaveMovementStatus
from apps.organizations.models import Role
from tests.authentication.factories import create_user, issue_access_token_for_user
from tests.blendes.factories import create_blave
from tests.organizations.factories import create_organization_with_membership


BLAVE_LIST_URL = "/api/v1/blaves/"


def blave_detail_url(blave_id, organization_id):
    return f"/api/v1/blaves/{blave_id}/?organization_id={organization_id}"


class BlavesAPITests(APITestCase):
    def authenticate(self, user):
        token = issue_access_token_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_requires_authentication(self):
        response = self.client.get(BLAVE_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"]["code"], "authentication_required")

    def test_list_returns_only_selected_organization_blaves(self):
        user = create_user(username="api-blave-list")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
        )
        other_organization, _ = create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
            name="API Other Blave Org",
        )
        expected = create_blave(
            organization=organization,
            created_by_user=user,
            title="Visible Blave",
        )
        create_blave(
            organization=other_organization,
            created_by_user=user,
            title="Hidden Blave",
        )

        self.authenticate(user)
        response = self.client.get(
            BLAVE_LIST_URL,
            {"organization_id": organization.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], expected.id)

    def test_owner_can_create_blave_and_initial_movements(self):
        user = create_user(username="api-blave-create-owner")
        organization, _ = create_organization_with_membership(user=user)
        self.authenticate(user)

        response = self.client.post(
            BLAVE_LIST_URL,
            {
                "organization_id": organization.id,
                "title": "API Blave",
                "description": "Criada pela API",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blave = Blave.objects.get(id=response.data["id"])
        self.assertEqual(blave.organization, organization)
        self.assertEqual(
            BlaveMovementStatus.objects.filter(blave=blave).count(),
            7,
        )

    def test_member_cannot_create_blave(self):
        user = create_user(username="api-blave-create-member")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
        )
        self.authenticate(user)

        response = self.client.post(
            BLAVE_LIST_URL,
            {
                "organization_id": organization.id,
                "title": "Bloqueada",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["error"]["code"], "user_not_admin_of_organization")

    def test_admin_can_patch_blave(self):
        user = create_user(username="api-blave-patch-admin")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.ADMIN,
        )
        blave = create_blave(organization=organization, created_by_user=user)
        self.authenticate(user)

        response = self.client.patch(
            blave_detail_url(blave.id, organization.id),
            {"title": "Atualizada"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blave.refresh_from_db()
        self.assertEqual(blave.title, "Atualizada")

    def test_owner_can_delete_blave(self):
        user = create_user(username="api-blave-delete-owner")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.OWNER,
        )
        blave = create_blave(organization=organization, created_by_user=user)
        self.authenticate(user)

        response = self.client.delete(
            blave_detail_url(blave.id, organization.id),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Blave.objects.filter(id=blave.id).exists())

    def test_member_cannot_delete_blave(self):
        user = create_user(username="api-blave-delete-member")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
        )
        blave = create_blave(organization=organization, created_by_user=user)
        self.authenticate(user)

        response = self.client.delete(
            blave_detail_url(blave.id, organization.id),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["error"]["code"], "user_not_admin_of_organization")
        self.assertTrue(Blave.objects.filter(id=blave.id).exists())
