"""Excecoes de dominio usadas pelo gerenciamento de praticas KREF."""


class KrefPraticeDomainError(Exception):
    """Excecao base para erros de dominio relacionados a praticas KREF."""

    code = "kref_pratice_error"
    message = "An error occurred in the KREF practice domain"

    def __init__(self):
        super().__init__(self.message)


class KrefPraticeBlaveNotFoundError(KrefPraticeDomainError):
    """Excecao para blave inexistente ou fora do escopo do usuario."""

    code = "kref_pratice_blave_not_found"
    message = "Blave not found"


class KrefPraticeBlaveInactiveOrganizationError(KrefPraticeDomainError):
    """Excecao para blave vinculada a uma organizacao inativa."""

    code = "kref_pratice_organization_inactive"
    message = "Organization is inactive"


class KrefPraticeMovementNotAllowedError(KrefPraticeDomainError):
    """Excecao para escrita fora do movimento echo."""

    code = "kref_pratice_movement_not_allowed"
    message = "KREF practices can only be managed during the ECHO movement"


class KrefPraticeBoundaryNotFoundError(KrefPraticeDomainError):
    """Excecao para boundary inexistente ou fora da blave informada."""

    code = "kref_pratice_boundary_not_found"
    message = "Boundary not found"


class KrefPraticeSchapterNotFoundError(KrefPraticeDomainError):
    """Excecao para schapter inexistente ou fora da boundary informada."""

    code = "kref_pratice_schapter_not_found"
    message = "Schapter not found"


class KrefPraticeFacetDescriptionNotFoundError(KrefPraticeDomainError):
    """Excecao para facet description inexistente ou fora da schapter."""

    code = "kref_pratice_facet_description_not_found"
    message = "Facet description not found"


class KrefPraticeRiskNotFoundError(KrefPraticeDomainError):
    """Excecao para risco inexistente ou fora da facet description."""

    code = "kref_pratice_risk_not_found"
    message = "Risk not found"


class KrefPraticeNotFoundError(KrefPraticeDomainError):
    """Excecao para pratica KREF inexistente ou fora do risco."""

    code = "kref_pratice_not_found"
    message = "KREF practice not found"
