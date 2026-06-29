"""Excecoes de dominio usadas pelo gerenciamento de riscos."""


class RiskDomainError(Exception):
    """Excecao base para erros de dominio relacionados a riscos."""

    code = "risk_error"
    message = "An error occurred in the risk domain"

    def __init__(self):
        super().__init__(self.message)


class RiskBlaveNotFoundError(RiskDomainError):
    """Excecao para blave inexistente ou fora do escopo do usuario."""

    code = "risk_blave_not_found"
    message = "Blave not found"


class RiskBlaveInactiveOrganizationError(RiskDomainError):
    """Excecao para blave vinculada a uma organizacao inativa."""

    code = "risk_organization_inactive"
    message = "Organization is inactive"


class RiskMovementNotAllowedError(RiskDomainError):
    """Excecao para escrita fora do movimento echo."""

    code = "risk_movement_not_allowed"
    message = "Risks can only be managed during the ECHO movement"


class RiskBoundaryNotFoundError(RiskDomainError):
    """Excecao para boundary inexistente ou fora da blave informada."""

    code = "risk_boundary_not_found"
    message = "Boundary not found"


class RiskSchapterNotFoundError(RiskDomainError):
    """Excecao para schapter inexistente ou fora da boundary informada."""

    code = "risk_schapter_not_found"
    message = "Schapter not found"


class RiskFacetDescriptionNotFoundError(RiskDomainError):
    """Excecao para facet description inexistente ou fora da schapter."""

    code = "risk_facet_description_not_found"
    message = "Facet description not found"


class RiskNotFoundError(RiskDomainError):
    """Excecao para risco inexistente ou fora da facet description."""

    code = "risk_not_found"
    message = "Risk not found"


class RiskFacetNotAllowedError(RiskDomainError):
    """Excecao para tentativa de criar risco em faceta sem geracao de risco."""

    code = "risk_facet_not_allowed"
    message = "This facet description cannot generate risks"
