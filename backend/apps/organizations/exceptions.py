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


class UserNotMemberOfOrganizationError(OrganizationDomainError):
    """Raised when the user is not a member of the organization."""

    code = "user_not_member_of_organization"
    message = "User is not a member of this organization"


class UserNotAdminOfOrganizationError(OrganizationDomainError):
    """Raised when the user cannot manage the organization."""

    code = "user_not_admin_of_organization"
    message = "User cannot manage this organization"
