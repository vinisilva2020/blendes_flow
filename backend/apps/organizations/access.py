from apps.organizations.exceptions import (
    OrganizationDomainError,
    OrganizationInactiveError,
    OrganizationNotFoundError,
    UserNotAdminOfOrganizationError,
    UserNotMemberOfOrganizationError,
)
from apps.organizations.models import OrganizationMembership


def _get_active_membership(user, organization_id):
    """Retorna a associação ativa do usuário com a organização informada."""
    membership = (
        OrganizationMembership.objects.select_related("organization")
        .only(
            "role",
            "organization_id",
            "organization__id",
            "organization__is_active",
        )
        .filter(
            user=user,
            organization_id=organization_id,
        )
        .first()
    )

    if membership is None:
        raise UserNotMemberOfOrganizationError

    if not membership.organization.is_active:
        raise OrganizationInactiveError

    return membership


def get_organization_for_read(user, organization_id):
    """Retorna uma organização ativa quando o usuário é membro dela."""
    return _get_active_membership(
        user=user,
        organization_id=organization_id,
    ).organization


def get_organization_for_manage(user, organization_id):
    """Retorna uma organização ativa quando o usuário pode gerenciá-la."""
    membership = _get_active_membership(
        user=user,
        organization_id=organization_id,
    )

    if not membership.can_manage:
        raise UserNotAdminOfOrganizationError

    return membership.organization


def get_organization_for_create(user, organization_id):
    """Retorna uma organização ativa quando o usuário pode criar registros nela."""
    return get_organization_for_manage(
        user=user,
        organization_id=organization_id,
    )


def get_organization_error_status(exc):
    """Retorna o status HTTP público para erros do domínio de organizações."""
    if isinstance(exc, UserNotAdminOfOrganizationError):
        return 403
    if isinstance(exc, OrganizationInactiveError):
        return 409
    if isinstance(exc, (OrganizationNotFoundError, UserNotMemberOfOrganizationError)):
        return 404
    return 400


__all__ = [
    "OrganizationDomainError",
    "get_organization_error_status",
    "get_organization_for_create",
    "get_organization_for_manage",
    "get_organization_for_read",
]
