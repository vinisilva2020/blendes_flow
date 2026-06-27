from django.db import transaction

from apps.blendes.exceptions.execution import (
    BlaveMovementSetupError,
    BlaveNotFoundError,
)
from apps.blendes.models.execution import (
    Blave,
    BlaveMovementStatus,
    Movement,
    MovementStatus,
)
from apps.blendes.querysets.execution import (
    find_organization_blave_for_update_queryset,
    find_organization_blave_queryset,
    list_organization_blaves_queryset,
)
from apps.organizations import access as organization_access


INITIAL_MOVEMENT_STATUSES = {
    Movement.BOUNDGROUND: MovementStatus.ACTIVE,
    Movement.LABOR: MovementStatus.LOCKED,
    Movement.ECHO: MovementStatus.LOCKED,
    Movement.NOISECATCH: MovementStatus.LOCKED,
    Movement.DRAWBRIDGE: MovementStatus.LOCKED,
    Movement.ENHANCE: MovementStatus.LOCKED,
    Movement.SIGHTLINE: MovementStatus.LOCKED,
}


def list_blaves_service(user, organization_id):
    """Lista as blaves da organização selecionada quando o usuário é membro."""
    organization = organization_access.get_organization_for_read(
        user=user,
        organization_id=organization_id,
    )
    return list_organization_blaves_queryset(organization=organization)


def get_blave_service(user, organization_id, blave_id):
    """Retorna uma blave da organização selecionada quando o usuário é membro."""
    organization = organization_access.get_organization_for_read(
        user=user,
        organization_id=organization_id,
    )
    blave = find_organization_blave_queryset(
        organization=organization,
        blave_id=blave_id,
    ).first()

    if blave is None:
        raise BlaveNotFoundError

    return blave


@transaction.atomic
def create_blave_service(user, organization_id, title, description=""):
    """Cria uma blave e seus movimentos iniciais em uma única transação."""
    organization = organization_access.get_organization_for_create(
        user=user,
        organization_id=organization_id,
    )

    blave = Blave(
        organization=organization,
        created_by_user=user,
        title=title,
        description=description or "",
    )
    blave.full_clean()
    blave.save()

    movement_statuses = [
        BlaveMovementStatus(
            blave=blave,
            movement=movement,
            status=status,
        )
        for movement, status in INITIAL_MOVEMENT_STATUSES.items()
    ]

    created_count = len(
        BlaveMovementStatus.objects.bulk_create(movement_statuses)
    )
    if created_count != len(INITIAL_MOVEMENT_STATUSES):
        raise BlaveMovementSetupError

    return get_blave_service(
        user=user,
        organization_id=organization_id,
        blave_id=blave.id,
    )


@transaction.atomic
def update_blave_service(
    user,
    organization_id,
    blave_id,
    title=None,
    description=None,
    status=None,
    current_movement=None,
):
    """Atualiza uma blave quando o usuário pode gerenciar a organização."""
    organization = organization_access.get_organization_for_manage(
        user=user,
        organization_id=organization_id,
    )
    blave = find_organization_blave_for_update_queryset(
        organization=organization,
        blave_id=blave_id,
    ).first()

    if blave is None:
        raise BlaveNotFoundError

    update_fields = []
    if title is not None:
        blave.title = title
        update_fields.append("title")
    if description is not None:
        blave.description = description
        update_fields.append("description")
    if status is not None:
        blave.status = status
        update_fields.append("status")
    if current_movement is not None:
        blave.current_movement = current_movement
        update_fields.append("current_movement")

    if not update_fields:
        return get_blave_service(
            user=user,
            organization_id=organization_id,
            blave_id=blave.id,
        )

    update_fields.append("updated_at")
    blave.full_clean()
    blave.save(update_fields=update_fields)

    return get_blave_service(
        user=user,
        organization_id=organization_id,
        blave_id=blave.id,
    )


@transaction.atomic
def delete_blave_service(user, organization_id, blave_id):
    """Exclui uma blave quando o usuário pode gerenciar a organização."""
    organization = organization_access.get_organization_for_manage(
        user=user,
        organization_id=organization_id,
    )
    blave = find_organization_blave_for_update_queryset(
        organization=organization,
        blave_id=blave_id,
    ).first()

    if blave is None:
        raise BlaveNotFoundError

    blave.delete()
