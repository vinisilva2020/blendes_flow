from django.db import transaction

from apps.blendes_flow.exceptions.boundaries import (
    BoundaryAlreadyExistsError,
    BoundaryBlaveInactiveOrganizationError,
    BoundaryBlaveNotFoundError,
    BoundaryHasChildrenError,
    BoundaryInvalidParentError,
    BoundaryMovementNotAllowedError,
    BoundaryNotFoundError,
    BoundaryOuterNotFoundError,
)
from apps.blendes_flow.models import Boundary, Movement
from apps.blendes_flow.querysets.boundaries import (
    blave_boundaries_queryset,
    boundary_in_blave_queryset,
    boundary_name_queryset,
    global_boundary_names_queryset,
    user_boundary_queryset,
    user_owned_blave_for_boundaries_queryset,
)

UNSET = object()


def _get_boundary_blave(user, blave_id):
    """Busca uma blave acessivel e traduz erros para o dominio boundary."""
    blave = user_owned_blave_for_boundaries_queryset(user).filter(id=blave_id).first()
    if blave is None:
        raise BoundaryBlaveNotFoundError
    if not blave.organization.is_active:
        raise BoundaryBlaveInactiveOrganizationError
    return blave


def _ensure_boundground(blave):
    """Garante que a blave esteja no movimento de gerenciamento de boundaries."""
    if blave.current_movement != Movement.BOUNDGROUND:
        raise BoundaryMovementNotAllowedError


def _get_boundary_in_blave(blave, boundary_id):
    """Busca uma boundary dentro da blave informada."""
    boundary = boundary_in_blave_queryset(blave).filter(id=boundary_id).first()
    if boundary is None:
        raise BoundaryNotFoundError
    return boundary


def _get_user_boundary(user, boundary_id):
    """Busca uma boundary acessivel usando somente o id dela."""
    boundary = user_boundary_queryset(user).filter(id=boundary_id).first()
    if boundary is None:
        raise BoundaryNotFoundError
    if not boundary.blave.organization.is_active:
        raise BoundaryBlaveInactiveOrganizationError
    return boundary


def _get_outer_boundary(blave, outer_boundary_id):
    """Busca uma boundary pai dentro da mesma blave."""
    outer_boundary = boundary_in_blave_queryset(blave).filter(id=outer_boundary_id).first()
    if outer_boundary is None:
        raise BoundaryOuterNotFoundError
    return outer_boundary


def _ensure_name_available(blave, name, ignored_boundary_id=None):
    """Impede nomes duplicados dentro de uma mesma blave."""
    query = boundary_name_queryset(blave=blave, name=name)
    if ignored_boundary_id is not None:
        query = query.exclude(id=ignored_boundary_id)
    if query.exists():
        raise BoundaryAlreadyExistsError


def _ensure_no_cycle(boundary, outer_boundary):
    """Impede que uma boundary seja ancestral dela mesma."""
    if outer_boundary is None:
        return

    current = outer_boundary
    while current is not None:
        if current.id == boundary.id:
            raise BoundaryInvalidParentError
        current = current.outer_boundary


def list_boundaries_service(user, blave_id, **_scope):
    """Lista boundaries de uma blave acessivel ao usuario."""
    blave = _get_boundary_blave(
        user=user,
        blave_id=blave_id,
    )
    return blave_boundaries_queryset(blave)


def list_global_boundary_names_service():
    """Lista nomes distintos de boundaries cadastradas para importacao."""
    return global_boundary_names_queryset()


def get_boundary_service(user, boundary_id, **_scope):
    """Retorna uma boundary da blave acessivel ao usuario."""
    return _get_user_boundary(user=user, boundary_id=boundary_id)


@transaction.atomic
def create_boundary_service(
    user,
    blave_id,
    name,
    description="",
    outer_boundary_id=None,
    outer_boundary_name=None,
    **_scope,
):
    """Cria uma boundary e opcionalmente cria a boundary pai por nome."""
    blave = _get_boundary_blave(
        user=user,
        blave_id=blave_id,
    )
    _ensure_boundground(blave)
    _ensure_name_available(blave=blave, name=name)

    outer_boundary = None
    if outer_boundary_id is not None:
        outer_boundary = _get_outer_boundary(
            blave=blave,
            outer_boundary_id=outer_boundary_id,
        )
    elif outer_boundary_name:
        if outer_boundary_name == name:
            raise BoundaryInvalidParentError
        outer_boundary, _ = Boundary.objects.get_or_create(
            blave=blave,
            name=outer_boundary_name,
            defaults={"description": ""},
        )

    boundary = Boundary(
        blave=blave,
        outer_boundary=outer_boundary,
        name=name,
        description=description,
    )
    boundary.full_clean()
    boundary.save()
    return _get_boundary_in_blave(blave=blave, boundary_id=boundary.id)


@transaction.atomic
def update_boundary_service(
    user,
    boundary_id,
    name=None,
    description=None,
    outer_boundary_id=UNSET,
    **_scope,
):
    """Atualiza campos permitidos de uma boundary."""
    boundary = _get_user_boundary(user=user, boundary_id=boundary_id)
    blave = boundary.blave
    _ensure_boundground(blave)

    if name is not None and name != boundary.name:
        _ensure_name_available(
            blave=blave,
            name=name,
            ignored_boundary_id=boundary.id,
        )
        boundary.name = name

    if description is not None:
        boundary.description = description

    if outer_boundary_id is not UNSET:
        if outer_boundary_id is None:
            outer_boundary = None
        else:
            outer_boundary = _get_outer_boundary(
                blave=blave,
                outer_boundary_id=outer_boundary_id,
            )
        _ensure_no_cycle(boundary=boundary, outer_boundary=outer_boundary)
        boundary.outer_boundary = outer_boundary

    boundary.full_clean()
    boundary.save()
    return _get_boundary_in_blave(blave=blave, boundary_id=boundary.id)


@transaction.atomic
def delete_boundary_service(user, boundary_id, **_scope):
    """Remove uma boundary somente quando nao existem filhas vinculadas."""
    boundary = _get_user_boundary(user=user, boundary_id=boundary_id)
    blave = boundary.blave
    _ensure_boundground(blave)

    if boundary.inner_boundaries.exists():
        raise BoundaryHasChildrenError

    boundary.delete()
