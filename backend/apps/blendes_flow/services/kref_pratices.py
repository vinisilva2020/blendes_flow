from django.db import transaction

from apps.blendes_flow.exceptions.kref_pratices import (
    KrefPraticeBlaveInactiveOrganizationError,
    KrefPraticeMovementNotAllowedError,
    KrefPraticeNotFoundError,
    KrefPraticeRiskNotFoundError,
)
from apps.blendes_flow.models import KrefPratice, Movement, Risk
from apps.blendes_flow.querysets.kref_pratices import (
    risk_kref_pratices_queryset,
    user_kref_pratice_queryset,
    user_risk_queryset,
)


def _ensure_echo(blave):
    """Garante que a blave esteja no movimento de gerenciamento de riscos."""
    if blave.current_movement != Movement.ECHO:
        raise KrefPraticeMovementNotAllowedError


def _get_user_risk(user, risk_id):
    """Busca um risco acessivel e deriva sua blave."""
    risk = user_risk_queryset(user).filter(id=risk_id).first()
    if risk is None:
        raise KrefPraticeRiskNotFoundError
    if not risk.facet_description.schapter.boundary.blave.organization.is_active:
        raise KrefPraticeBlaveInactiveOrganizationError
    return risk


def _get_user_kref_pratice(user, kref_pratice_id):
    """Busca uma pratica KREF acessivel usando somente o id dela."""
    kref_pratice = user_kref_pratice_queryset(user).filter(id=kref_pratice_id).first()
    if kref_pratice is None:
        raise KrefPraticeNotFoundError
    if not kref_pratice.risk.facet_description.schapter.boundary.blave.organization.is_active:
        raise KrefPraticeBlaveInactiveOrganizationError
    return kref_pratice


def list_kref_pratices_service(user, risk_id, **_scope):
    """Lista praticas KREF de um risco acessivel ao usuario."""
    risk = _get_user_risk(user=user, risk_id=risk_id)
    return risk_kref_pratices_queryset(risk)


def get_kref_pratice_service(user, kref_pratice_id, **_scope):
    """Retorna uma pratica KREF acessivel ao usuario."""
    return _get_user_kref_pratice(user=user, kref_pratice_id=kref_pratice_id)


@transaction.atomic
def create_kref_pratices_service(user, risk_id, kref_pratices, **_scope):
    """Cria praticas KREF de um risco em uma unica transacao."""
    risk = _get_user_risk(user=user, risk_id=risk_id)
    blave = risk.facet_description.schapter.boundary.blave
    _ensure_echo(blave)

    kref_pratice_instances = [
        KrefPratice(
            risk=risk,
            pratice=item["pratice"],
            references=item["references"],
        )
        for item in kref_pratices
    ]
    for kref_pratice in kref_pratice_instances:
        kref_pratice.full_clean()

    KrefPratice.objects.bulk_create(kref_pratice_instances)
    return list_kref_pratices_service(user=user, risk_id=risk_id)


@transaction.atomic
def update_kref_pratice_service(
    user,
    kref_pratice_id,
    pratice=None,
    references=None,
    **_scope,
):
    """Atualiza campos permitidos de uma pratica KREF."""
    kref_pratice = _get_user_kref_pratice(
        user=user,
        kref_pratice_id=kref_pratice_id,
    )
    blave = kref_pratice.risk.facet_description.schapter.boundary.blave
    _ensure_echo(blave)

    if pratice is not None:
        kref_pratice.pratice = pratice
    if references is not None:
        kref_pratice.references = references

    kref_pratice.full_clean()
    kref_pratice.save()
    return _get_user_kref_pratice(
        user=user,
        kref_pratice_id=kref_pratice.id,
    )


@transaction.atomic
def delete_kref_pratice_service(user, kref_pratice_id, **_scope):
    """Remove uma pratica KREF acessivel ao usuario."""
    kref_pratice = _get_user_kref_pratice(
        user=user,
        kref_pratice_id=kref_pratice_id,
    )
    blave = kref_pratice.risk.facet_description.schapter.boundary.blave
    _ensure_echo(blave)
    kref_pratice.delete()
