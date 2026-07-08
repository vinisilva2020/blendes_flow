class OrganizationDomainError(Exception):
    """Excecao base para erros de dominio relacionados a organizacoes."""

    code = "organization_error"
    message = "An error occurred in the organization domain"

    def __init__(self):
        super().__init__(self.message)


class OrganizationNotFoundError(OrganizationDomainError):
    """Excecao para organizacao nao encontrada."""

    code = "organization_not_found"
    message = "Organization not found"


class OrganizationInactiveError(OrganizationDomainError):
    """Excecao para organizacao inativa."""

    code = "organization_inactive"
    message = "Organization is inactive"


class OrganizationAlreadyExistsError(OrganizationDomainError):
    """Excecao para organizacao que ja existe."""

    code = "organization_already_exists"
    message = "Organization with this name already exists"
