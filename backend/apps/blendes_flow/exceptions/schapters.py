"""Excecoes de dominio usadas pelo gerenciamento de schapters."""


class SchapterDomainError(Exception):
    """Excecao base para erros de dominio relacionados a schapters."""

    code = "schapter_error"
    message = "An error occurred in the schapter domain"

    def __init__(self):
        super().__init__(self.message)


class SchapterBlaveNotFoundError(SchapterDomainError):
    """Excecao para blave inexistente ou fora do escopo do usuario."""

    code = "schapter_blave_not_found"
    message = "Blave not found"


class SchapterBlaveInactiveOrganizationError(SchapterDomainError):
    """Excecao para blave vinculada a uma organizacao inativa."""

    code = "schapter_organization_inactive"
    message = "Organization is inactive"


class SchapterMovementNotAllowedError(SchapterDomainError):
    """Excecao para escrita fora do movimento labor."""

    code = "schapter_movement_not_allowed"
    message = "Schapters can only be managed during the LABOR movement"


class SchapterBoundaryNotFoundError(SchapterDomainError):
    """Excecao para boundary inexistente ou fora da blave informada."""

    code = "schapter_boundary_not_found"
    message = "Boundary not found"


class SchapterNotFoundError(SchapterDomainError):
    """Excecao para schapter inexistente ou fora da boundary informada."""

    code = "schapter_not_found"
    message = "Schapter not found"


class SchapterAlreadyExistsError(SchapterDomainError):
    """Excecao para nome duplicado dentro da mesma boundary."""

    code = "schapter_already_exists"
    message = "Schapter already exists in this boundary"


class SchapterRoleTypeConflictError(SchapterDomainError):
    """Excecao para role existente com tipo diferente do solicitado."""

    code = "schapter_role_type_conflict"
    message = "Role already exists with a different type"
