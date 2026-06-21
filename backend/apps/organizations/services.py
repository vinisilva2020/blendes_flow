from django.db import IntegrityError
from django.db import transaction

from apps.organizations.exceptions import (
    OrganizationAlreadyExistsError,
    OrganizationInactiveError,
    UserNotAdminOfOrganizationError,
    UserNotMemberOfOrganizationError,
)
from apps.organizations.models import Organization, OrganizationMembership, Role


def list_user_organizations_service(user):
    """List active organizations where the user is a member."""
    return Organization.objects.filter(
        memberships__user=user,
        is_active=True,
    ).order_by("name")


def _get_user_membership_with_organization(user, organization_id):
    membership = (
        OrganizationMembership.objects.select_related("organization")
        .only(
            "role",
            "organization_id",
            "organization__id",
            "organization__name",
            "organization__description",
            "organization__is_active",
            "organization__created_by",
            "organization__created_at",
            "organization__updated_at",
        )
        .filter(user=user, organization_id=organization_id)
        .first()
    )

    if membership is None:
        raise UserNotMemberOfOrganizationError

    if not membership.organization.is_active:
        raise OrganizationInactiveError

    return membership


def get_user_organization_service(user, organization_id):
    """Get an active organization when the user is a member."""
    membership = _get_user_membership_with_organization(
        user=user,
        organization_id=organization_id,
    )
    organization = membership.organization
    organization._current_user_membership_role = membership.role
    return organization


@transaction.atomic
def create_organization_service(user, name: str, description=""):
    """Create an organization and make the user its owner."""
    try:
        org = Organization.objects.create(
            name=name,
            description=description,
            created_by=user,
        )
    except IntegrityError:
        raise OrganizationAlreadyExistsError

    OrganizationMembership.objects.create(
        user=user,
        organization=org,
        role=Role.OWNER,
    )

    return org


@transaction.atomic
def update_organization_service(user, organization_id, name=None, description=None):
    """Update an organization when the user can manage it."""
    membership = _get_user_membership_with_organization(
        user=user,
        organization_id=organization_id,
    )

    if not membership.can_manage:
        raise UserNotAdminOfOrganizationError

    organization = membership.organization
    update_fields = []

    if name is not None:
        organization.name = name
        update_fields.append("name")

    if description is not None:
        organization.description = description
        update_fields.append("description")

    if not update_fields:
        return organization

    update_fields.append("updated_at")
    organization.full_clean()
    try:
        organization.save(update_fields=update_fields)
    except IntegrityError:
        raise OrganizationAlreadyExistsError

    return organization


@transaction.atomic
def delete_organization_service(user, organization_id):
    """Delete an organization when the user can manage it."""
    membership = _get_user_membership_with_organization(
        user=user,
        organization_id=organization_id,
    )

    if not membership.can_manage:
        raise UserNotAdminOfOrganizationError

    membership.organization.delete()
