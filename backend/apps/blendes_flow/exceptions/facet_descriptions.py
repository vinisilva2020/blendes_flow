"""Excecoes de dominio usadas pelo gerenciamento de facet descriptions."""


class FacetDescriptionDomainError(Exception):
    """Excecao base para erros de dominio relacionados a facet descriptions."""

    code = "facet_description_error"
    message = "An error occurred in the facet description domain"

    def __init__(self):
        super().__init__(self.message)


class FacetDescriptionBlaveNotFoundError(FacetDescriptionDomainError):
    """Excecao para blave inexistente ou fora do escopo do usuario."""

    code = "facet_description_blave_not_found"
    message = "Blave not found"


class FacetDescriptionBlaveInactiveOrganizationError(FacetDescriptionDomainError):
    """Excecao para blave vinculada a uma organizacao inativa."""

    code = "facet_description_organization_inactive"
    message = "Organization is inactive"


class FacetDescriptionMovementNotAllowedError(FacetDescriptionDomainError):
    """Excecao para escrita fora do movimento echo."""

    code = "facet_description_movement_not_allowed"
    message = "Facet descriptions can only be managed during the ECHO movement"


class FacetDescriptionBoundaryNotFoundError(FacetDescriptionDomainError):
    """Excecao para boundary inexistente ou fora da blave informada."""

    code = "facet_description_boundary_not_found"
    message = "Boundary not found"


class FacetDescriptionSchapterNotFoundError(FacetDescriptionDomainError):
    """Excecao para schapter inexistente ou fora da boundary informada."""

    code = "facet_description_schapter_not_found"
    message = "Schapter not found"


class FacetDescriptionNotFoundError(FacetDescriptionDomainError):
    """Excecao para facet description inexistente ou fora da schapter."""

    code = "facet_description_not_found"
    message = "Facet description not found"


class FacetDescriptionAlreadyExistsError(FacetDescriptionDomainError):
    """Excecao para faceta ja cadastrada dentro da schapter."""

    code = "facet_description_already_exists"
    message = "Facet description already exists in this schapter"
