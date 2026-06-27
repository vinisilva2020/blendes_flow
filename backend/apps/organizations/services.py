from django.db import IntegrityError
from django.db import transaction

from apps.organizations.exceptions import (
    OrganizationAlreadyExistsError,
    OrganizationInactiveError,
    OrganizationNotFoundError,
)
from apps.organizations.models import Organization


def list_user_organizations_service(user):
    """List active organizations created by the user."""
    return Organization.objects.filter(
        created_by=user,
        is_active=True,
    ).order_by("name")


def _get_user_owned_organization(user, organization_id):
    organization = (
        Organization.objects.only(
            "id",
            "name",
            "description",
            "is_active",
            "created_by",
            "created_at",
            "updated_at",
        )
        .filter(created_by=user, id=organization_id)
        .first()
    )

    if organization is None:
        raise OrganizationNotFoundError

    if not organization.is_active:
        raise OrganizationInactiveError

    return organization


def get_user_organization_service(user, organization_id):
    """Get an active organization created by the user."""
    return _get_user_owned_organization(
        user=user,
        organization_id=organization_id,
    )


@transaction.atomic
def create_organization_service(user, name: str, description=""):
    """Create an organization owned by the authenticated user."""
    try:
        return Organization.objects.create(
            name=name,
            description=description,
            created_by=user,
        )
    except IntegrityError:
        raise OrganizationAlreadyExistsError


@transaction.atomic
def update_organization_service(user, organization_id, name=None, description=None):
    """Update an organization created by the user."""
    organization = _get_user_owned_organization(
        user=user,
        organization_id=organization_id,
    )
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
    """Delete an organization created by the user."""
    organization = _get_user_owned_organization(
        user=user,
        organization_id=organization_id,
    )
    organization.delete()
