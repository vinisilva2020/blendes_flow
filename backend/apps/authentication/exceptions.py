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


class GoogleAuthenticationNotConfiguredError(AuthenticationDomainError):
    """Excecao para autenticacao Google sem client ID configurado."""

    code = "google_authentication_not_configured"
    message = "Google authentication is not configured"


class InvalidGoogleCredentialError(AuthenticationDomainError):
    """Excecao para credenciais Google invalidas."""

    code = "invalid_google_credential"
    message = "Invalid Google credential provided"


class UnverifiedGoogleEmailError(AuthenticationDomainError):
    """Excecao para conta Google sem email verificado."""

    code = "unverified_google_email"
    message = "Google account email is not verified"


class GoogleAccountHostedDomainError(AuthenticationDomainError):
    """Excecao para conta Google fora do dominio permitido."""

    code = "invalid_google_hosted_domain"
    message = "Google account is not allowed for this application"


class GoogleAccountConflictError(AuthenticationDomainError):
    """Excecao para email Google ja associado a uma conta local."""

    code = "google_account_conflict"
    message = "A local account already exists for this email"
