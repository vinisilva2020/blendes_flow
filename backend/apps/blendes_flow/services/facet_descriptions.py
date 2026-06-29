from django.db import transaction

from apps.blendes_flow.exceptions.facet_descriptions import (
    FacetDescriptionAlreadyExistsError,
    FacetDescriptionBlaveInactiveOrganizationError,
    FacetDescriptionBoundaryNotFoundError,
    FacetDescriptionMovementNotAllowedError,
    FacetDescriptionNotFoundError,
    FacetDescriptionSchapterNotFoundError,
)
from apps.blendes_flow.models import (
    FacetDescription,
    FacetType,
    Movement,
)
from apps.blendes_flow.querysets.facet_descriptions import (
    boundary_in_blave_queryset,
    facet_description_in_schapter_queryset,
    facet_descriptions_by_facets_queryset,
    schapter_facet_descriptions_queryset,
    schapter_in_boundary_queryset,
    user_facet_description_queryset,
    user_schapter_queryset,
)

UNSET = object()


def _ensure_echo(blave):
    """Garante que a blave esteja no movimento de gerenciamento de facetas."""
    if blave.current_movement != Movement.ECHO:
        raise FacetDescriptionMovementNotAllowedError


def _get_boundary_in_blave(blave, boundary_id):
    """Busca uma boundary dentro da blave informada."""
    boundary = boundary_in_blave_queryset(blave).filter(id=boundary_id).first()
    if boundary is None:
        raise FacetDescriptionBoundaryNotFoundError
    return boundary


def _get_schapter_in_boundary(boundary, schapter_id):
    """Busca uma schapter dentro da boundary informada."""
    schapter = schapter_in_boundary_queryset(boundary).filter(id=schapter_id).first()
    if schapter is None:
        raise FacetDescriptionSchapterNotFoundError
    return schapter


def _get_facet_description_in_schapter(schapter, facet_description_id):
    """Busca uma facet description dentro da schapter informada."""
    facet_description = facet_description_in_schapter_queryset(schapter).filter(
        id=facet_description_id,
    ).first()
    if facet_description is None:
        raise FacetDescriptionNotFoundError
    return facet_description


def _get_user_schapter(user, schapter_id):
    """Busca uma schapter acessivel e deriva sua blave."""
    schapter = user_schapter_queryset(user).filter(id=schapter_id).first()
    if schapter is None:
        raise FacetDescriptionSchapterNotFoundError
    if not schapter.boundary.blave.organization.is_active:
        raise FacetDescriptionBlaveInactiveOrganizationError
    return schapter


def _get_user_facet_description(user, facet_description_id):
    """Busca uma facet description acessivel usando somente o id dela."""
    facet_description = user_facet_description_queryset(user).filter(
        id=facet_description_id,
    ).first()
    if facet_description is None:
        raise FacetDescriptionNotFoundError
    if not facet_description.schapter.boundary.blave.organization.is_active:
        raise FacetDescriptionBlaveInactiveOrganizationError
    return facet_description


def _normalize_generate_risk(facet, generate_risk):
    """Aplica a regra que impede geracao de risco pela faceta WHAT."""
    if facet == FacetType.WHAT:
        return False
    return generate_risk


def _ensure_facets_available(schapter, facets):
    """Impede cadastro duplicado de facetas para uma mesma schapter."""
    facet_names = [item["facet"] for item in facets]
    if facet_descriptions_by_facets_queryset(
        schapter=schapter,
        facet_names=facet_names,
    ).exists():
        raise FacetDescriptionAlreadyExistsError


def _get_schapter_context(user, schapter_id):
    """Retorna a schapter validando escopo de organizacao, blave e boundary."""
    schapter = _get_user_schapter(user=user, schapter_id=schapter_id)
    return schapter.boundary.blave, schapter


def list_facet_descriptions_service(
    user,
    schapter_id,
    **_scope,
):
    """Lista facet descriptions de uma schapter acessivel ao usuario."""
    _, schapter = _get_schapter_context(
        user=user,
        schapter_id=schapter_id,
    )
    return schapter_facet_descriptions_queryset(schapter)


def get_facet_description_service(
    user,
    facet_description_id,
    **_scope,
):
    """Retorna uma facet description da schapter acessivel ao usuario."""
    return _get_user_facet_description(
        user=user,
        facet_description_id=facet_description_id,
    )


@transaction.atomic
def create_facet_descriptions_service(
    user,
    schapter_id,
    facets,
    **_scope,
):
    """Cria todas as facet descriptions da schapter em uma unica transacao."""
    blave, schapter = _get_schapter_context(
        user=user,
        schapter_id=schapter_id,
    )
    _ensure_echo(blave)
    _ensure_facets_available(schapter=schapter, facets=facets)

    facet_descriptions = [
        FacetDescription(
            schapter=schapter,
            facet=item["facet"],
            generate_risk=_normalize_generate_risk(
                facet=item["facet"],
                generate_risk=item.get("generate_risk", True),
            ),
            value=item["value"],
            observation=item.get("observation"),
        )
        for item in facets
    ]
    for facet_description in facet_descriptions:
        facet_description.full_clean()

    FacetDescription.objects.bulk_create(facet_descriptions)
    return list_facet_descriptions_service(
        user=user,
        schapter_id=schapter_id,
    )


@transaction.atomic
def update_facet_description_service(
    user,
    facet_description_id,
    generate_risk=UNSET,
    value=None,
    observation=UNSET,
    **_scope,
):
    """Atualiza campos permitidos de uma facet description."""
    facet_description = _get_user_facet_description(
        user=user,
        facet_description_id=facet_description_id,
    )
    schapter = facet_description.schapter
    blave = schapter.boundary.blave
    _ensure_echo(blave)

    if generate_risk is not UNSET:
        facet_description.generate_risk = _normalize_generate_risk(
            facet=facet_description.facet,
            generate_risk=generate_risk,
        )
    if value is not None:
        facet_description.value = value
    if observation is not UNSET:
        facet_description.observation = observation

    facet_description.full_clean()
    facet_description.save()
    return _get_facet_description_in_schapter(
        schapter=schapter,
        facet_description_id=facet_description.id,
    )


@transaction.atomic
def delete_facet_description_service(
    user,
    facet_description_id,
    **_scope,
):
    """Remove uma facet description da schapter acessivel ao usuario."""
    facet_description = _get_user_facet_description(
        user=user,
        facet_description_id=facet_description_id,
    )
    blave = facet_description.schapter.boundary.blave
    _ensure_echo(blave)
    facet_description.delete()
