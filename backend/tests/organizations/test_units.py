from django.test import RequestFactory, TestCase

from apps.organizations.api.v1.serializers import (
    OrganizationInputSerializerV1,
    OrganizationOutputSerializerV1,
)
from apps.organizations.permissions import IsOrganizationOwner
from tests.authentication.factories import create_user
from tests.organizations.factories import create_organization


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
        self.permission = IsOrganizationOwner()
        self.factory = RequestFactory()

    def test_owner_can_access_organization(self):
        user = create_user(username="permission-owner")
        organization = create_organization(created_by=user)
        request = self.factory.get("/")
        request.user = user

        allowed = self.permission.has_object_permission(
            request,
            view=None,
            obj=organization,
        )

        self.assertTrue(allowed)

    def test_other_user_cannot_access_organization(self):
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
