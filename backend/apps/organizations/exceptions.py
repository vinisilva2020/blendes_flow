class OrganizationDomainError(Exception):
    """Exceção base para erros de domínio relacionados a organizações."""

    code = "organization_error"
    message = "An error occurred in the organization domain"

    def __init__(self):
        super().__init__(self.message)


class OrganizationNotFoundError(OrganizationDomainError):
    """Exceção para organização não encontrada."""

    code = "organization_not_found"
    message = "Organization not found"


class UserNotMemberOfOrganizationError(OrganizationDomainError):
    """Exceção para usuário que não é membro da organização."""

    code = "user_not_member_of_organization"
    message = "User is not a member of the organization"


class UserAlreadyMemberOfOrganizationError(OrganizationDomainError):
    """Exceção para usuário que já é membro da organização."""

    code = "user_already_member_of_organization"
    message = "User is already a member of the organization"


class UserNotAdminOfOrganizationError(OrganizationDomainError):
    """Exceção para usuário que não é admin da organização."""

    code = "user_not_admin_of_organization"
    message = "User is not an admin of the organization"


class OrganizationInactiveError(OrganizationDomainError):
    """Exceção para organização inativa."""

    code = "organization_inactive"
    message = "Organization is inactive"


class OrganizationAlreadyExistsError(OrganizationDomainError):
    """Exceção para organização que já existe."""

    code = "organization_already_exists"
    message = "Organization with this name already exists"
