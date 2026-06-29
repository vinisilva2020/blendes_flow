"""Excecoes de dominio usadas pelo gerenciamento de blaves."""


class BlaveDomainError(Exception):
    """Excecao base para erros de dominio relacionados a blaves."""

    code = "blave_error"
    message = "An error occurred in the blave domain"

    def __init__(self):
        super().__init__(self.message)


class BlaveNotFoundError(BlaveDomainError):
    """Excecao para blave nao encontrada ou fora do escopo do usuario."""

    code = "blave_not_found"
    message = "Blave not found"


class BlaveOrganizationNotFoundError(BlaveDomainError):
    """Excecao para organizacao inexistente ou nao criada pelo usuario."""

    code = "blave_organization_not_found"
    message = "Organization not found"


class BlaveOrganizationInactiveError(BlaveDomainError):
    """Excecao para organizacao inativa usada no cadastro de blaves."""

    code = "blave_organization_inactive"
    message = "Organization is inactive"
