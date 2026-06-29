from dataclasses import dataclass

from apps.organizations.models import Organization


@dataclass(frozen=True)
class OrganizationAccessDTO:
    """Dados minimos expostos para integracao com outros apps."""

    id: int
    is_active: bool


def get_user_owned_organization_access(user, organization_id):
    """Retorna os dados publicos de acesso de uma organizacao do usuario."""
    organization = (
        Organization.objects.only("id", "is_active")
        .filter(id=organization_id, created_by=user)
        .first()
    )

    if organization is None:
        return None

    return OrganizationAccessDTO(
        id=organization.id,
        is_active=organization.is_active,
    )
