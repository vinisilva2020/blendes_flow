class AuthenticationDomainError(Exception):
    """Exceção base para erros de domínio relacionados à autenticação."""

    code = "authentication_error"
    message = "Authentication could not be completed"

    def __init__(self):
        super().__init__(self.message)


class InvalidCredentialsError(AuthenticationDomainError):
    """Exceção para credenciais inválidas."""

    code = "invalid_credentials"
    message = "Invalid credentials provided"


class InvalidRefreshTokenError(AuthenticationDomainError):
    """Exceção para tokens de atualização inválidos."""

    code = "invalid_refresh_token"
    message = "Invalid refresh token provided"


class AuthenticationSessionNotFoundError(AuthenticationDomainError):
    """Exceção para sessões de autenticação não encontradas."""

    code = "authentication_session_not_found"
    message = "Authentication session not found"
