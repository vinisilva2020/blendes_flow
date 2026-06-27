class BlaveDomainError(Exception):
    """Erro base para regras de domínio relacionadas a blaves."""

    code = "blave_domain_error"
    message = "Erro de domínio da blave."


class BlaveNotFoundError(BlaveDomainError):
    """Indica que a blave não existe ou não pertence ao escopo permitido."""

    code = "blave_not_found"
    message = "Blave não encontrada."


class BlaveMovementSetupError(BlaveDomainError):
    """Indica falha ao preparar os movimentos iniciais de uma blave."""

    code = "blave_movement_setup_error"
    message = "Não foi possível preparar os movimentos iniciais da blave."
