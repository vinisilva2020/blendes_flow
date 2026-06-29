from django.db import transaction

from apps.blendes_flow.exceptions.blaves import (
    BlaveNotFoundError,
    BlaveOrganizationInactiveError,
    BlaveOrganizationNotFoundError,
)
from apps.blendes_flow.models import Blave, BlaveMovements, Movement, MovementStatus
from apps.blendes_flow.querysets.blaves import (
    organization_blaves_queryset,
    user_owned_blave_in_organization_queryset,
    user_owned_blave_queryset,
)
from apps.organizations.access import get_user_owned_organization_access


def _get_user_owned_active_organization_dto(user, organization_id):
    """Busca o DTO de uma organizacao ativa criada pelo usuario."""
    organization = get_user_owned_organization_access(
        user=user,
        organization_id=organization_id,
    )

    if organization is None:
        raise BlaveOrganizationNotFoundError

    if not organization.is_active:
        raise BlaveOrganizationInactiveError

    return organization


def _get_user_owned_blave(user, organization_id, blave_id):
    """Busca uma blave dentro de uma organizacao acessivel ao usuario."""
    organization = _get_user_owned_active_organization_dto(
        user=user,
        organization_id=organization_id,
    )
    blave = user_owned_blave_in_organization_queryset(organization).filter(
        id=blave_id,
    ).first()

    if blave is None:
        raise BlaveNotFoundError

    return blave


def _get_user_owned_blave_by_id(user, blave_id):
    """Busca uma blave acessivel usando apenas seu identificador."""
    blave = user_owned_blave_queryset(user).filter(id=blave_id).first()

    if blave is None:
        raise BlaveNotFoundError

    if not blave.organization.is_active:
        raise BlaveOrganizationInactiveError

    return blave


def list_blaves_service(user, organization_id):
    """Lista blaves de uma organizacao ativa criada pelo usuario."""
    organization = _get_user_owned_active_organization_dto(
        user=user,
        organization_id=organization_id,
    )
    return organization_blaves_queryset(organization)


def get_blave_service(user, blave_id, **_scope):
    """Retorna uma blave do usuario autenticado."""
    return _get_user_owned_blave_by_id(user=user, blave_id=blave_id)


@transaction.atomic
def create_blave_service(user, organization_id, title: str):
    """Cria uma blave e inicializa todos os movimentos do fluxo."""
    organization = _get_user_owned_active_organization_dto(
        user=user,
        organization_id=organization_id,
    )
    blave = Blave(
        organization_id=organization.id,
        created_by_user=user,
        title=title,
    )
    blave.full_clean()
    blave.save()

    movements = [
        BlaveMovements(
            blave=blave,
            movement=movement,
            status=(
                MovementStatus.ACTIVE
                if movement == Movement.BOUNDGROUND
                else MovementStatus.LOCKED
            ),
        )
        for movement in Movement.values
    ]
    BlaveMovements.objects.bulk_create(movements)

    return _get_user_owned_blave(
        user=user,
        organization_id=organization_id,
        blave_id=blave.id,
    )


@transaction.atomic
def update_blave_service(user, blave_id, title=None, **_scope):
    """Atualiza apenas o titulo de uma blave criada pelo usuario."""
    blave = _get_user_owned_blave_by_id(user=user, blave_id=blave_id)

    if title is None:
        return blave

    blave.title = title
    blave.full_clean()
    blave.save(update_fields=["title", "updated_at"])
    return blave


@transaction.atomic
def delete_blave_service(user, blave_id, **_scope):
    """Remove uma blave criada dentro da organizacao do usuario."""
    blave = _get_user_owned_blave_by_id(user=user, blave_id=blave_id)
    blave.delete()
