"""Excecoes de dominio usadas pelo gerenciamento de mixpoints."""


class MixpointDomainError(Exception):
    """Excecao base para erros de dominio relacionados a mixpoints."""

    code = "mixpoint_error"
    message = "An error occurred in the mixpoint domain"

    def __init__(self):
        super().__init__(self.message)


class MixpointBlaveNotFoundError(MixpointDomainError):
    """Excecao para blave inexistente ou fora do escopo do usuario."""

    code = "mixpoint_blave_not_found"
    message = "Blave not found"


class MixpointBlaveInactiveOrganizationError(MixpointDomainError):
    """Excecao para blave vinculada a uma organizacao inativa."""

    code = "mixpoint_organization_inactive"
    message = "Organization is inactive"


class MixpointMovementNotAllowedError(MixpointDomainError):
    """Excecao para escrita fora do movimento sightline."""

    code = "mixpoint_movement_not_allowed"
    message = "Mixpoints can only be managed during the SIGHTLINE movement"


class MixpointBoundaryNotFoundError(MixpointDomainError):
    """Excecao para boundary inexistente ou fora da blave informada."""

    code = "mixpoint_boundary_not_found"
    message = "Boundary not found"


class MixpointSchapterNotFoundError(MixpointDomainError):
    """Excecao para schapter inexistente ou fora da boundary informada."""

    code = "mixpoint_schapter_not_found"
    message = "Schapter not found"


class MixpointFacetDescriptionNotFoundError(MixpointDomainError):
    """Excecao para facet description inexistente ou fora da schapter."""

    code = "mixpoint_facet_description_not_found"
    message = "Facet description not found"


class MixpointRiskNotFoundError(MixpointDomainError):
    """Excecao para risco inexistente ou fora da facet description."""

    code = "mixpoint_risk_not_found"
    message = "Risk not found"


class MixpointKrefPraticeNotFoundError(MixpointDomainError):
    """Excecao para pratica KREF inexistente ou fora do risco."""

    code = "mixpoint_kref_pratice_not_found"
    message = "KREF practice not found"


class MixpointConcreteActionNotFoundError(MixpointDomainError):
    """Excecao para acao concreta inexistente ou fora da pratica KREF."""

    code = "mixpoint_concrete_action_not_found"
    message = "Concrete action not found"


class MixpointNotFoundError(MixpointDomainError):
    """Excecao para mixpoint inexistente ou fora da acao concreta."""

    code = "mixpoint_not_found"
    message = "Mixpoint not found"
