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
