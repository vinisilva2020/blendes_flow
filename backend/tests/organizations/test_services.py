from django.test import TestCase

from apps.organizations.exceptions import (
    OrganizationAlreadyExistsError,
    OrganizationInactiveError,
    UserNotAdminOfOrganizationError,
    UserNotMemberOfOrganizationError,
)
from apps.organizations.models import Organization, OrganizationMembership, Role
from apps.organizations.services import (
    create_organization_service,
    delete_organization_service,
    get_user_organization_service,
    list_user_organizations_service,
    update_organization_service,
)
from tests.authentication.factories import create_user
from tests.organizations.factories import (
    create_membership,
    create_organization,
    create_organization_with_membership,
)


class ListUserOrganizationsServiceTests(TestCase):
    def test_lists_only_active_organizations_where_user_is_member(self):
        user = create_user(username="list-user")
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
        create_organization(name="Outside Org")

        organizations = list(list_user_organizations_service(user))

        self.assertEqual(organizations, [active_org])


class GetUserOrganizationServiceTests(TestCase):
    def test_returns_organization_for_member_and_stores_current_role(self):
        user = create_user(username="detail-user")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.ADMIN,
        )

        result = get_user_organization_service(user, organization.id)

        self.assertEqual(result, organization)
        self.assertEqual(result._current_user_membership_role, Role.ADMIN)

    def test_raises_when_user_is_not_member(self):
        user = create_user(username="detail-outsider")
        organization = create_organization()

        with self.assertRaises(UserNotMemberOfOrganizationError):
            get_user_organization_service(user, organization.id)

    def test_raises_when_organization_is_inactive(self):
        user = create_user(username="detail-inactive")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
            is_active=False,
        )

        with self.assertRaises(OrganizationInactiveError):
            get_user_organization_service(user, organization.id)


class CreateOrganizationServiceTests(TestCase):
    def test_creates_organization_and_owner_membership(self):
        user = create_user(username="create-owner")

        organization = create_organization_service(
            user=user,
            name="Created Org",
            description="Created description",
        )

        self.assertEqual(organization.created_by, user)
        self.assertTrue(
            OrganizationMembership.objects.filter(
                user=user,
                organization=organization,
                role=Role.OWNER,
            ).exists()
        )

    def test_raises_domain_error_for_duplicate_name(self):
        user = create_user(username="create-duplicate")
        create_organization(name="Duplicate Org")

        with self.assertRaises(OrganizationAlreadyExistsError):
            create_organization_service(user=user, name="Duplicate Org")


class UpdateOrganizationServiceTests(TestCase):
    def test_owner_can_update_organization(self):
        user = create_user(username="update-owner")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.OWNER,
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

    def test_admin_can_update_organization(self):
        owner = create_user(username="update-owner")
        admin = create_user(username="update-admin")
        organization = create_organization(created_by=owner)
        create_membership(user=admin, organization=organization, role=Role.ADMIN)

        update_organization_service(
            user=admin,
            organization_id=organization.id,
            name="Admin Updated",
        )

        organization.refresh_from_db()
        self.assertEqual(organization.name, "Admin Updated")

    def test_member_cannot_update_organization(self):
        user = create_user(username="update-member")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
        )

        with self.assertRaises(UserNotAdminOfOrganizationError):
            update_organization_service(
                user=user,
                organization_id=organization.id,
                name="Forbidden Update",
            )

    def test_noop_update_returns_organization_without_saving_fields(self):
        user = create_user(username="update-noop")
        organization, _ = create_organization_with_membership(user=user)

        result = update_organization_service(
            user=user,
            organization_id=organization.id,
        )

        self.assertEqual(result, organization)


class DeleteOrganizationServiceTests(TestCase):
    def test_owner_can_delete_organization(self):
        user = create_user(username="delete-owner")
        organization, _ = create_organization_with_membership(user=user)

        delete_organization_service(user=user, organization_id=organization.id)

        self.assertFalse(Organization.objects.filter(id=organization.id).exists())

    def test_member_cannot_delete_organization(self):
        user = create_user(username="delete-member")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
        )

        with self.assertRaises(UserNotAdminOfOrganizationError):
            delete_organization_service(user=user, organization_id=organization.id)

        self.assertTrue(Organization.objects.filter(id=organization.id).exists())
