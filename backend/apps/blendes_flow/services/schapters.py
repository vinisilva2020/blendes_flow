from django.db import transaction

from apps.blendes_flow.exceptions.schapters import (
    SchapterAlreadyExistsError,
    SchapterBlaveInactiveOrganizationError,
    SchapterBoundaryNotFoundError,
    SchapterMovementNotAllowedError,
    SchapterNotFoundError,
    SchapterRoleTypeConflictError,
)
from apps.blendes_flow.models import Boundary, Movement, Role, RoleExecutionSchapter, Schapter
from apps.blendes_flow.querysets.schapters import (
    boundary_in_blave_queryset,
    boundary_schapters_queryset,
    global_schapter_names_queryset,
    schapter_in_boundary_queryset,
    schapter_name_queryset,
    user_boundary_queryset,
    user_schapter_queryset,
)

UNSET = object()


def _ensure_labor(blave):
    """Garante que a blave esteja no movimento de gerenciamento de schapters."""
    if blave.current_movement != Movement.LABOR:
        raise SchapterMovementNotAllowedError


def _get_boundary_in_blave(blave, boundary_id):
    """Busca uma boundary dentro da blave informada."""
    boundary = boundary_in_blave_queryset(blave).filter(id=boundary_id).first()
    if boundary is None:
        raise SchapterBoundaryNotFoundError
    return boundary


def _get_user_boundary(user, boundary_id):
    """Busca uma boundary acessivel e deriva sua blave."""
    boundary = user_boundary_queryset(user).filter(id=boundary_id).first()
    if boundary is None:
        raise SchapterBoundaryNotFoundError
    if not boundary.blave.organization.is_active:
        raise SchapterBlaveInactiveOrganizationError
    return boundary


def _get_user_schapter(user, schapter_id):
    """Busca uma schapter acessivel usando somente o id dela."""
    schapter = user_schapter_queryset(user).filter(id=schapter_id).first()
    if schapter is None:
        raise SchapterNotFoundError
    if not schapter.boundary.blave.organization.is_active:
        raise SchapterBlaveInactiveOrganizationError
    return schapter


def _get_schapter_in_boundary(boundary, schapter_id):
    """Busca uma schapter dentro da boundary informada."""
    schapter = schapter_in_boundary_queryset(boundary).filter(id=schapter_id).first()
    if schapter is None:
        raise SchapterNotFoundError
    return schapter


def _ensure_name_available(boundary, name, ignored_schapter_id=None):
    """Impede nomes duplicados dentro de uma mesma boundary."""
    query = schapter_name_queryset(boundary=boundary, name=name)
    if ignored_schapter_id is not None:
        query = query.exclude(id=ignored_schapter_id)
    if query.exists():
        raise SchapterAlreadyExistsError


def _get_or_create_roles(organization_id, roles):
    """Cria ou reutiliza roles da organizacao para vinculo com schapters."""
    resolved_roles = []
    for role_data in roles:
        role, created = Role.objects.get_or_create(
            organization_id=organization_id,
            name=role_data["name"],
            defaults={"type": role_data["type"]},
        )
        if not created and role.type != role_data["type"]:
            raise SchapterRoleTypeConflictError
        resolved_roles.append(role)
    return resolved_roles


def _replace_role_executions(schapter, roles):
    """Substitui os vinculos de execucao de roles de forma performatica."""
    RoleExecutionSchapter.objects.filter(schapter=schapter).delete()
    RoleExecutionSchapter.objects.bulk_create(
        [
            RoleExecutionSchapter(schapter=schapter, role=role)
            for role in roles
        ],
        ignore_conflicts=True,
    )


def list_schapters_service(user, boundary_id, **_scope):
    """Lista schapters de uma boundary acessivel ao usuario."""
    boundary = _get_user_boundary(user=user, boundary_id=boundary_id)
    return boundary_schapters_queryset(boundary)


def list_global_schapter_names_service():
    """Lista nomes distintos de schapters cadastradas para importacao."""
    return global_schapter_names_queryset()


def get_schapter_service(
    user,
    schapter_id,
    **_scope,
):
    """Retorna uma schapter da boundary acessivel ao usuario."""
    return _get_user_schapter(user=user, schapter_id=schapter_id)


@transaction.atomic
def create_schapter_service(
    user,
    boundary_id,
    name,
    roles,
    **_scope,
):
    """Cria uma schapter e suas roles executoras em uma unica transacao."""
    boundary = _get_user_boundary(user=user, boundary_id=boundary_id)
    blave = boundary.blave
    _ensure_labor(blave)
    _ensure_name_available(boundary=boundary, name=name)

    schapter = Schapter(boundary=boundary, name=name)
    schapter.full_clean()
    schapter.save()

    resolved_roles = _get_or_create_roles(
        organization_id=blave.organization_id,
        roles=roles,
    )
    _replace_role_executions(schapter=schapter, roles=resolved_roles)

    return _get_schapter_in_boundary(
        boundary=boundary,
        schapter_id=schapter.id,
    )


@transaction.atomic
def update_schapter_service(
    user,
    schapter_id,
    name=None,
    roles=UNSET,
    **_scope,
):
    """Atualiza campos permitidos de uma schapter."""
    schapter = _get_user_schapter(user=user, schapter_id=schapter_id)
    boundary = schapter.boundary
    blave = boundary.blave
    _ensure_labor(blave)

    if name is not None and name != schapter.name:
        _ensure_name_available(
            boundary=boundary,
            name=name,
            ignored_schapter_id=schapter.id,
        )
        schapter.name = name
        schapter.full_clean()
        schapter.save(update_fields=["name", "updated_at"])

    if roles is not UNSET:
        resolved_roles = _get_or_create_roles(
            organization_id=blave.organization_id,
            roles=roles,
        )
        _replace_role_executions(schapter=schapter, roles=resolved_roles)

    return _get_schapter_in_boundary(
        boundary=boundary,
        schapter_id=schapter.id,
    )


@transaction.atomic
def delete_schapter_service(
    user,
    schapter_id,
    **_scope,
):
    """Remove uma schapter da boundary acessivel ao usuario."""
    schapter = _get_user_schapter(user=user, schapter_id=schapter_id)
    blave = schapter.boundary.blave
    _ensure_labor(blave)
    schapter.delete()
