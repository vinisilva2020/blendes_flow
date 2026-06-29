from django.db import transaction

from apps.blendes_flow.exceptions.mixpoints import (
    MixpointBlaveInactiveOrganizationError,
    MixpointConcreteActionNotFoundError,
    MixpointMovementNotAllowedError,
    MixpointNotFoundError,
)
from apps.blendes_flow.models import ConcreteAction, Mixpoint, Movement
from apps.blendes_flow.querysets.mixpoints import (
    concrete_action_mixpoints_queryset,
    user_concrete_action_queryset,
    user_mixpoint_queryset,
)


def _ensure_sightline(blave):
    """Garante que a blave esteja no movimento de gerenciamento de mixpoints."""
    if blave.current_movement != Movement.SIGHTLINE:
        raise MixpointMovementNotAllowedError


def _get_user_concrete_action(user, concrete_action_id):
    """Busca uma acao concreta acessivel e deriva sua blave."""
    concrete_action = user_concrete_action_queryset(user).filter(
        id=concrete_action_id,
    ).first()
    if concrete_action is None:
        raise MixpointConcreteActionNotFoundError
    blave = concrete_action.kref_pratice.risk.facet_description.schapter.boundary.blave
    if not blave.organization.is_active:
        raise MixpointBlaveInactiveOrganizationError
    return concrete_action


def _get_user_mixpoint(user, mixpoint_id):
    """Busca um mixpoint acessivel usando somente o id dele."""
    mixpoint = user_mixpoint_queryset(user).filter(id=mixpoint_id).first()
    if mixpoint is None:
        raise MixpointNotFoundError
    blave = mixpoint.concrete_action.kref_pratice.risk.facet_description.schapter.boundary.blave
    if not blave.organization.is_active:
        raise MixpointBlaveInactiveOrganizationError
    return mixpoint


def list_mixpoints_service(user, concrete_action_id, **_scope):
    """Lista mixpoints de uma acao concreta acessivel ao usuario."""
    concrete_action = _get_user_concrete_action(
        user=user,
        concrete_action_id=concrete_action_id,
    )
    return concrete_action_mixpoints_queryset(concrete_action)


def get_mixpoint_service(user, mixpoint_id, **_scope):
    """Retorna um mixpoint acessivel ao usuario."""
    return _get_user_mixpoint(user=user, mixpoint_id=mixpoint_id)


@transaction.atomic
def create_mixpoints_service(user, concrete_action_id, mixpoints, **_scope):
    """Cria mixpoints de uma acao concreta em uma unica transacao."""
    concrete_action = _get_user_concrete_action(
        user=user,
        concrete_action_id=concrete_action_id,
    )
    blave = concrete_action.kref_pratice.risk.facet_description.schapter.boundary.blave
    _ensure_sightline(blave)

    mixpoint_instances = [
        Mixpoint(
            concrete_action=concrete_action,
            description=item["description"],
        )
        for item in mixpoints
    ]
    for mixpoint in mixpoint_instances:
        mixpoint.full_clean()

    Mixpoint.objects.bulk_create(mixpoint_instances)
    return list_mixpoints_service(
        user=user,
        concrete_action_id=concrete_action_id,
    )


@transaction.atomic
def update_mixpoint_service(user, mixpoint_id, description=None, **_scope):
    """Atualiza campos permitidos de um mixpoint."""
    mixpoint = _get_user_mixpoint(user=user, mixpoint_id=mixpoint_id)
    blave = mixpoint.concrete_action.kref_pratice.risk.facet_description.schapter.boundary.blave
    _ensure_sightline(blave)

    if description is not None:
        mixpoint.description = description

    mixpoint.full_clean()
    mixpoint.save()
    return _get_user_mixpoint(user=user, mixpoint_id=mixpoint.id)


@transaction.atomic
def delete_mixpoint_service(user, mixpoint_id, **_scope):
    """Remove um mixpoint acessivel ao usuario."""
    mixpoint = _get_user_mixpoint(user=user, mixpoint_id=mixpoint_id)
    blave = mixpoint.concrete_action.kref_pratice.risk.facet_description.schapter.boundary.blave
    _ensure_sightline(blave)
    mixpoint.delete()
