from django.db import transaction

from apps.blendes_flow.exceptions.risks import (
    RiskBlaveInactiveOrganizationError,
    RiskBoundaryNotFoundError,
    RiskFacetDescriptionNotFoundError,
    RiskFacetNotAllowedError,
    RiskMovementNotAllowedError,
    RiskNotFoundError,
    RiskSchapterNotFoundError,
)
from apps.blendes_flow.models import (
    FacetDescription,
    FacetType,
    Movement,
    Risk,
)
from apps.blendes_flow.querysets.risks import (
    boundary_in_blave_queryset,
    facet_description_in_schapter_queryset,
    facet_description_risks_queryset,
    risk_in_facet_description_queryset,
    schapter_in_boundary_queryset,
    user_facet_description_queryset,
    user_risk_queryset,
)

UNSET = object()


def _ensure_echo(blave):
    """Garante que a blave esteja no movimento de gerenciamento de riscos."""
    if blave.current_movement != Movement.ECHO:
        raise RiskMovementNotAllowedError


def _get_boundary_in_blave(blave, boundary_id):
    """Busca uma boundary dentro da blave informada."""
    boundary = boundary_in_blave_queryset(blave).filter(id=boundary_id).first()
    if boundary is None:
        raise RiskBoundaryNotFoundError
    return boundary


def _get_schapter_in_boundary(boundary, schapter_id):
    """Busca uma schapter dentro da boundary informada."""
    schapter = schapter_in_boundary_queryset(boundary).filter(id=schapter_id).first()
    if schapter is None:
        raise RiskSchapterNotFoundError
    return schapter


def _get_facet_description_in_schapter(schapter, facet_description_id):
    """Busca uma facet description dentro da schapter informada."""
    facet_description = facet_description_in_schapter_queryset(schapter).filter(
        id=facet_description_id,
    ).first()
    if facet_description is None:
        raise RiskFacetDescriptionNotFoundError
    return facet_description


def _get_risk_in_facet_description(facet_description, risk_id):
    """Busca um risco dentro da facet description informada."""
    risk = risk_in_facet_description_queryset(facet_description).filter(
        id=risk_id,
    ).first()
    if risk is None:
        raise RiskNotFoundError
    return risk


def _get_user_facet_description(user, facet_description_id):
    """Busca uma facet description acessivel e deriva sua blave."""
    facet_description = user_facet_description_queryset(user).filter(
        id=facet_description_id,
    ).first()
    if facet_description is None:
        raise RiskFacetDescriptionNotFoundError
    if not facet_description.schapter.boundary.blave.organization.is_active:
        raise RiskBlaveInactiveOrganizationError
    return facet_description


def _get_user_risk(user, risk_id):
    """Busca um risco acessivel usando somente o id dele."""
    risk = user_risk_queryset(user).filter(id=risk_id).first()
    if risk is None:
        raise RiskNotFoundError
    if not risk.facet_description.schapter.boundary.blave.organization.is_active:
        raise RiskBlaveInactiveOrganizationError
    return risk


def _ensure_facet_generates_risk(facet_description):
    """Impede riscos em facetas que nao podem gerar risco."""
    if facet_description.facet == FacetType.WHAT or not facet_description.generate_risk:
        raise RiskFacetNotAllowedError


def _get_facet_description_context(
    user,
    facet_description_id,
):
    """Retorna a blave e a facet description validando todo o escopo."""
    facet_description = _get_user_facet_description(
        user=user,
        facet_description_id=facet_description_id,
    )
    blave = facet_description.schapter.boundary.blave
    return blave, facet_description


def list_risks_service(
    user,
    facet_description_id,
    **_scope,
):
    """Lista riscos de uma facet description acessivel ao usuario."""
    _, facet_description = _get_facet_description_context(
        user=user,
        facet_description_id=facet_description_id,
    )
    return facet_description_risks_queryset(facet_description)


def get_risk_service(
    user,
    risk_id,
    **_scope,
):
    """Retorna um risco da facet description acessivel ao usuario."""
    return _get_user_risk(user=user, risk_id=risk_id)


@transaction.atomic
def create_risks_service(
    user,
    facet_description_id,
    risks,
    **_scope,
):
    """Cria riscos de uma facet description em uma unica transacao."""
    blave, facet_description = _get_facet_description_context(
        user=user,
        facet_description_id=facet_description_id,
    )
    _ensure_echo(blave)
    _ensure_facet_generates_risk(facet_description)

    risk_instances = [
        Risk(
            facet_description=facet_description,
            formated_text=item["formated_text"],
            strategic_impact=item["strategic_impact"],
            operational_impact=item["operational_impact"],
            tactical_impact=item["tactical_impact"],
        )
        for item in risks
    ]
    for risk in risk_instances:
        risk.full_clean()

    Risk.objects.bulk_create(risk_instances)
    return list_risks_service(
        user=user,
        facet_description_id=facet_description_id,
    )


@transaction.atomic
def update_risk_service(
    user,
    risk_id,
    formated_text=None,
    strategic_impact=None,
    operational_impact=None,
    tactical_impact=None,
    **_scope,
):
    """Atualiza campos permitidos de um risco."""
    risk = _get_user_risk(user=user, risk_id=risk_id)
    facet_description = risk.facet_description
    blave = facet_description.schapter.boundary.blave
    _ensure_echo(blave)
    _ensure_facet_generates_risk(facet_description)

    if formated_text is not None:
        risk.formated_text = formated_text
    if strategic_impact is not None:
        risk.strategic_impact = strategic_impact
    if operational_impact is not None:
        risk.operational_impact = operational_impact
    if tactical_impact is not None:
        risk.tactical_impact = tactical_impact

    risk.full_clean()
    risk.save()
    return _get_risk_in_facet_description(
        facet_description=facet_description,
        risk_id=risk.id,
    )


@transaction.atomic
def delete_risk_service(
    user,
    risk_id,
    **_scope,
):
    """Remove um risco da facet description acessivel ao usuario."""
    risk = _get_user_risk(user=user, risk_id=risk_id)
    blave = risk.facet_description.schapter.boundary.blave
    _ensure_echo(blave)
    risk.delete()
