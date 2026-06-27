from django.test import TestCase

from apps.organizations.exceptions import (
    OrganizationAlreadyExistsError,
    OrganizationInactiveError,
    OrganizationNotFoundError,
)
from apps.organizations.models import Organization
from apps.organizations.services import (
    create_organization_service,
    delete_organization_service,
    get_user_organization_service,
    list_user_organizations_service,
    update_organization_service,
)
from tests.authentication.factories import create_user
from tests.organizations.factories import create_organization


class ListUserOrganizationsServiceTests(TestCase):
    def test_lists_only_active_organizations_created_by_user(self):
        user = create_user(username="list-user")
        other_user = create_user(username="list-other")
        active_org = create_organization(
            created_by=user,
            name="Active Org",
        )
        create_organization(
            created_by=user,
            name="Inactive Org",
            is_active=False,
        )
        create_organization(created_by=other_user, name="Outside Org")

        organizations = list(list_user_organizations_service(user))

        self.assertEqual(organizations, [active_org])


class GetUserOrganizationServiceTests(TestCase):
    def test_returns_organization_created_by_user(self):
        user = create_user(username="detail-user")
        organization = create_organization(created_by=user)

        result = get_user_organization_service(user, organization.id)

        self.assertEqual(result, organization)

    def test_raises_when_user_does_not_own_organization(self):
        user = create_user(username="detail-outsider")
        organization = create_organization()

        with self.assertRaises(OrganizationNotFoundError):
            get_user_organization_service(user, organization.id)

    def test_raises_when_organization_is_inactive(self):
        user = create_user(username="detail-inactive")
        organization = create_organization(
            created_by=user,
            is_active=False,
        )

        with self.assertRaises(OrganizationInactiveError):
            get_user_organization_service(user, organization.id)


class CreateOrganizationServiceTests(TestCase):
    def test_creates_organization_owned_by_user(self):
        user = create_user(username="create-owner")

        organization = create_organization_service(
            user=user,
            name="Created Org",
            description="Created description",
        )

        self.assertEqual(organization.created_by, user)
        self.assertEqual(organization.name, "Created Org")

    def test_raises_domain_error_for_duplicate_name(self):
        user = create_user(username="create-duplicate")
        create_organization(name="Duplicate Org")

        with self.assertRaises(OrganizationAlreadyExistsError):
            create_organization_service(user=user, name="Duplicate Org")


class UpdateOrganizationServiceTests(TestCase):
    def test_owner_can_update_organization(self):
        user = create_user(username="update-owner")
        organization = create_organization(
            created_by=user,
            name="Old Name",
        )

        result = update_organization_service(
            user=user,
            organization_id=organization.id,
            name="New Name",
            description="New description",
        )

        organization.refresh_from_db()
        self.assertEqual(result, organization)
        self.assertEqual(organization.name, "New Name")
        self.assertEqual(organization.description, "New description")

    def test_other_user_cannot_update_organization(self):
        user = create_user(username="update-outsider")
        organization = create_organization()

        with self.assertRaises(OrganizationNotFoundError):
            update_organization_service(
                user=user,
                organization_id=organization.id,
                name="Forbidden Update",
            )

    def test_noop_update_returns_organization_without_saving_fields(self):
        user = create_user(username="update-noop")
        organization = create_organization(created_by=user)

        result = update_organization_service(
            user=user,
            organization_id=organization.id,
        )

        self.assertEqual(result, organization)


class DeleteOrganizationServiceTests(TestCase):
    def test_owner_can_delete_organization(self):
        user = create_user(username="delete-owner")
        organization = create_organization(created_by=user)

        delete_organization_service(user=user, organization_id=organization.id)

        self.assertFalse(Organization.objects.filter(id=organization.id).exists())

    def test_other_user_cannot_delete_organization(self):
        user = create_user(username="delete-outsider")
        organization = create_organization()

        with self.assertRaises(OrganizationNotFoundError):
            delete_organization_service(user=user, organization_id=organization.id)

        self.assertTrue(Organization.objects.filter(id=organization.id).exists())
