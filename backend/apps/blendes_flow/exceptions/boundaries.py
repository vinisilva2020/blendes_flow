"""Excecoes de dominio usadas pelo gerenciamento de boundaries."""


class BoundaryDomainError(Exception):
    """Excecao base para erros de dominio relacionados a boundaries."""

    code = "boundary_error"
    message = "An error occurred in the boundary domain"

    def __init__(self):
        super().__init__(self.message)


class BoundaryBlaveNotFoundError(BoundaryDomainError):
    """Excecao para blave inexistente ou fora do escopo do usuario."""

    code = "boundary_blave_not_found"
    message = "Blave not found"


class BoundaryBlaveInactiveOrganizationError(BoundaryDomainError):
    """Excecao para blave vinculada a uma organizacao inativa."""

    code = "boundary_organization_inactive"
    message = "Organization is inactive"


class BoundaryMovementNotAllowedError(BoundaryDomainError):
    """Excecao para escrita fora do movimento boundground."""

    code = "boundary_movement_not_allowed"
    message = "Boundaries can only be managed during the BOUNDGROUND movement"


class BoundaryNotFoundError(BoundaryDomainError):
    """Excecao para boundary inexistente ou fora da blave informada."""

    code = "boundary_not_found"
    message = "Boundary not found"


class BoundaryOuterNotFoundError(BoundaryDomainError):
    """Excecao para boundary pai inexistente ou fora da blave informada."""

    code = "boundary_outer_not_found"
    message = "Outer boundary not found"


class BoundaryInvalidParentError(BoundaryDomainError):
    """Excecao para relacionamento hierarquico invalido."""

    code = "boundary_invalid_parent"
    message = "Boundary hierarchy is invalid"


class BoundaryAlreadyExistsError(BoundaryDomainError):
    """Excecao para nome duplicado dentro da mesma blave."""

    code = "boundary_already_exists"
    message = "Boundary already exists in this blave"


class BoundaryHasChildrenError(BoundaryDomainError):
    """Excecao para remocao de boundary com filhas vinculadas."""

    code = "boundary_has_children"
    message = "Boundary has inner boundaries"
