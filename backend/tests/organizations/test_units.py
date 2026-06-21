from django.test import RequestFactory, TestCase

from apps.organizations.api.v1.serializers import (
    OrganizationInputSerializerV1,
    OrganizationOutputSerializerV1,
)
from apps.organizations.models import Role
from apps.organizations.permissions import (
    IsOrganizationMemberReadOnlyOrAdminOwnerWrite,
)
from tests.authentication.factories import create_user
from tests.organizations.factories import (
    create_membership,
    create_organization,
    create_organization_with_membership,
)


class OrganizationMembershipUnitTests(TestCase):
    def test_owner_and_admin_can_manage_organization(self):
        owner_membership = create_membership(role=Role.OWNER)
        admin_membership = create_membership(role=Role.ADMIN)

        self.assertTrue(owner_membership.can_manage)
        self.assertTrue(admin_membership.can_manage)

    def test_member_cannot_manage_organization(self):
        membership = create_membership(role=Role.MEMBER)

        self.assertFalse(membership.can_manage)


class OrganizationSerializerUnitTests(TestCase):
    def test_input_serializer_trims_name_and_accepts_blank_description(self):
        serializer = OrganizationInputSerializerV1(
            data={
                "name": "  Blend ES  ",
                "description": "",
            },
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["name"], "Blend ES")
        self.assertEqual(serializer.validated_data["description"], "")

    def test_output_serializer_exposes_public_fields(self):
        organization = create_organization(name="Public Org")

        data = OrganizationOutputSerializerV1(organization).data

        self.assertEqual(data["name"], "Public Org")
        self.assertIn("id", data)
        self.assertIn("is_active", data)
        self.assertNotIn("created_by", data)


class OrganizationPermissionUnitTests(TestCase):
    def setUp(self):
        self.permission = IsOrganizationMemberReadOnlyOrAdminOwnerWrite()
        self.factory = RequestFactory()

    def test_members_can_read_organization(self):
        user = create_user(username="permission-member")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
        )
        request = self.factory.get("/")
        request.user = user

        allowed = self.permission.has_object_permission(
            request,
            view=None,
            obj=organization,
        )

        self.assertTrue(allowed)

    def test_members_cannot_write_organization(self):
        user = create_user(username="permission-member")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
        )
        request = self.factory.patch("/")
        request.user = user

        allowed = self.permission.has_object_permission(
            request,
            view=None,
            obj=organization,
        )

        self.assertFalse(allowed)

    def test_admins_can_write_organization_when_role_is_prefetched(self):
        user = create_user(username="permission-admin")
        organization = create_organization(created_by=user)
        organization._current_user_membership_role = Role.ADMIN
        request = self.factory.patch("/")
        request.user = user

        allowed = self.permission.has_object_permission(
            request,
            view=None,
            obj=organization,
        )

        self.assertTrue(allowed)

    def test_non_members_cannot_read_organization(self):
        user = create_user(username="permission-outsider")
        organization = create_organization()
        request = self.factory.get("/")
        request.user = user

        allowed = self.permission.has_object_permission(
            request,
            view=None,
            obj=organization,
        )

        self.assertFalse(allowed)
