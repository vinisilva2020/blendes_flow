from django.test import TestCase

from apps.blendes.exceptions.execution import BlaveNotFoundError
from apps.blendes.models.execution import BlaveMovementStatus, Movement, MovementStatus
from apps.blendes.services.execution import (
    INITIAL_MOVEMENT_STATUSES,
    create_blave_service,
    delete_blave_service,
    list_blaves_service,
    update_blave_service,
)
from apps.organizations.exceptions import (
    UserNotAdminOfOrganizationError,
    UserNotMemberOfOrganizationError,
)
from apps.organizations.models import Role
from tests.authentication.factories import create_user
from tests.blendes.factories import create_blave
from tests.organizations.factories import (
    create_membership,
    create_organization,
    create_organization_with_membership,
)


class ListBlavesServiceTests(TestCase):
    def test_lists_blaves_only_from_selected_member_organization(self):
        user = create_user(username="blave-list-member")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
        )
        other_organization, _ = create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
            name="Other Blave Org",
        )
        expected = create_blave(
            organization=organization,
            created_by_user=user,
            title="Selected Org Blave",
        )
        create_blave(
            organization=other_organization,
            created_by_user=user,
            title="Other Org Blave",
        )

        result = list(list_blaves_service(user, organization.id))

        self.assertEqual(result, [expected])

    def test_raises_when_user_is_not_member_of_selected_organization(self):
        user = create_user(username="blave-list-outsider")
        organization = create_organization()

        with self.assertRaises(UserNotMemberOfOrganizationError):
            list_blaves_service(user, organization.id)


class CreateBlaveServiceTests(TestCase):
    def test_owner_creates_blave_with_initial_movement_statuses(self):
        user = create_user(username="blave-create-owner")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.OWNER,
        )

        blave = create_blave_service(
            user=user,
            organization_id=organization.id,
            title="Nova blave",
            description="Descrição inicial",
        )

        self.assertEqual(blave.organization, organization)
        self.assertEqual(blave.created_by_user, user)
        statuses = {
            item.movement: item.status
            for item in BlaveMovementStatus.objects.filter(blave=blave)
        }
        self.assertEqual(statuses, INITIAL_MOVEMENT_STATUSES)
        self.assertEqual(statuses[Movement.BOUNDGROUND], MovementStatus.ACTIVE)

    def test_member_cannot_create_blave(self):
        user = create_user(username="blave-create-member")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
        )

        with self.assertRaises(UserNotAdminOfOrganizationError):
            create_blave_service(
                user=user,
                organization_id=organization.id,
                title="Bloqueada",
            )


class UpdateBlaveServiceTests(TestCase):
    def test_admin_can_update_blave_inside_selected_organization(self):
        owner = create_user(username="blave-update-owner")
        admin = create_user(username="blave-update-admin")
        organization = create_organization(created_by=owner)
        create_membership(user=admin, organization=organization, role=Role.ADMIN)
        blave = create_blave(organization=organization, created_by_user=owner)

        result = update_blave_service(
            user=admin,
            organization_id=organization.id,
            blave_id=blave.id,
            title="Título atualizado",
            current_movement=Movement.LABOR,
        )

        blave.refresh_from_db()
        self.assertEqual(result.id, blave.id)
        self.assertEqual(blave.title, "Título atualizado")
        self.assertEqual(blave.current_movement, Movement.LABOR)

    def test_does_not_update_blave_from_another_organization(self):
        user = create_user(username="blave-update-wrong-org")
        selected_organization, _ = create_organization_with_membership(user=user)
        other_organization = create_organization(name="Wrong Blave Org")
        blave = create_blave(organization=other_organization)

        with self.assertRaises(BlaveNotFoundError):
            update_blave_service(
                user=user,
                organization_id=selected_organization.id,
                blave_id=blave.id,
                title="Não deve alterar",
            )


class DeleteBlaveServiceTests(TestCase):
    def test_owner_can_delete_blave_inside_selected_organization(self):
        user = create_user(username="blave-delete-owner")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.OWNER,
        )
        blave = create_blave(organization=organization, created_by_user=user)

        delete_blave_service(
            user=user,
            organization_id=organization.id,
            blave_id=blave.id,
        )

        self.assertFalse(type(blave).objects.filter(id=blave.id).exists())

    def test_member_cannot_delete_blave(self):
        user = create_user(username="blave-delete-member")
        organization, _ = create_organization_with_membership(
            user=user,
            role=Role.MEMBER,
        )
        blave = create_blave(organization=organization, created_by_user=user)

        with self.assertRaises(UserNotAdminOfOrganizationError):
            delete_blave_service(
                user=user,
                organization_id=organization.id,
                blave_id=blave.id,
            )

        self.assertTrue(type(blave).objects.filter(id=blave.id).exists())

    def test_does_not_delete_blave_from_another_organization(self):
        user = create_user(username="blave-delete-wrong-org")
        selected_organization, _ = create_organization_with_membership(user=user)
        other_organization = create_organization(name="Delete Wrong Blave Org")
        blave = create_blave(organization=other_organization)

        with self.assertRaises(BlaveNotFoundError):
            delete_blave_service(
                user=user,
                organization_id=selected_organization.id,
                blave_id=blave.id,
            )

        self.assertTrue(type(blave).objects.filter(id=blave.id).exists())
