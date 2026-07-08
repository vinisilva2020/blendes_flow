class AccountDomainError(Exception):
    """Base exception for account domain errors."""

    code = "account_error"
    message = "An error occurred in the account domain"

    def __init__(self):
        super().__init__(self.message)


class AccountAlreadyExistsError(AccountDomainError):
    """Raised when username or email is already registered."""

    code = "account_already_exists"
    message = "Account with this username or email already exists"


class AccountInactiveError(AccountDomainError):
    """Raised when an inactive account is accessed."""

    code = "account_inactive"
    message = "Account is inactive"


class SocialAccountNotFoundError(AccountDomainError):
    """Raised when a linked social account cannot be found for the user."""

    code = "social_account_not_found"
    message = "Social account not found"


class SocialAccountConflictError(AccountDomainError):
    """Raised when a social account cannot be linked to this user."""

    code = "social_account_conflict"
    message = "Social account cannot be linked to this account"


class InvalidSocialAccountCredentialError(AccountDomainError):
    """Raised when an external social account credential is invalid."""

    code = "invalid_social_account_credential"
    message = "Invalid social account credential provided"


class UnverifiedSocialAccountEmailError(AccountDomainError):
    """Raised when an external social account email is not verified."""

    code = "unverified_social_account_email"
    message = "Social account email is not verified"


class SocialAccountHostedDomainError(AccountDomainError):
    """Raised when an external social account is outside the allowed domain."""

    code = "invalid_social_account_hosted_domain"
    message = "Social account is not allowed for this application"


class LastAuthenticationMethodError(AccountDomainError):
    """Raised when unlinking would leave the user without a login method."""

    code = "last_authentication_method"
    message = "Cannot unlink the last authentication method"


class InvalidCurrentPasswordError(AccountDomainError):
    """Raised when the submitted current password does not match."""

    code = "invalid_current_password"
    message = "Current password is invalid"
