import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import authenticate
from django.db import transaction
from django.utils import timezone

from apps.authentication.exceptions import (
    AuthenticationSessionNotFoundError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
)
from apps.authentication.models import (
    AuthenticationSession,
    AuthenticationTokens,
)


def authenticate_user_service(identifier, password):
    """Autentica um usuário com base no identificador e senha fornecidos."""
    user = authenticate(username=identifier, password=password)
    if user is None or not user.is_active:
        raise InvalidCredentialsError

    refresh_secret = AuthenticationTokens.generate_refresh_secret()
    session = AuthenticationSession.objects.create(
        user=user,
        refresh_token_hash=AuthenticationTokens.hash_refresh_token(refresh_secret),
        expires_at=timezone.now()
        + timedelta(seconds=settings.AUTH_SESSION_LIFETIME_SECONDS),
    )
    return AuthenticationTokens.issue_authentication_tokens(
        session=session, refresh_secret=refresh_secret
    )


@transaction.atomic
def refresh_authentication_session_service(refresh_token):
    """Renova uma sessão de autenticação utilizando um token de atualização."""
    parsed = AuthenticationTokens.parse_refresh_token(refresh_token)
    if parsed is None:
        raise InvalidRefreshTokenError
    session_id, secret = parsed
    session = (
        AuthenticationSession.objects.select_for_update()
        .select_related("user")
        .filter(id=session_id)
        .first()
    )
    if session is None:
        raise InvalidRefreshTokenError
    is_valid_secret = secrets.compare_digest(
        session.refresh_token_hash,
        AuthenticationTokens.hash_refresh_token(secret),
    )
    if not is_valid_secret or not session.is_active or not session.user.is_active:
        raise InvalidRefreshTokenError

    new_refresh_secret = AuthenticationTokens.generate_refresh_secret()
    session.refresh_token_hash = AuthenticationTokens.hash_refresh_token(
        new_refresh_secret
    )
    session.last_used_at = timezone.now()
    session.save(update_fields=["refresh_token_hash", "last_used_at", "updated_at"])

    return AuthenticationTokens.issue_authentication_tokens(
        session=session, refresh_secret=new_refresh_secret
    )


@transaction.atomic
def revoke_authentication_session_service(session_id, user_id):
    """Revoga de forma idempotente uma sessão pertencente ao usuário autenticado."""
    session = (
        AuthenticationSession.objects.select_for_update()
        .filter(id=session_id, user_id=user_id)
        .first()
    )

    if session is None:
        return AuthenticationSessionNotFoundError

    if session.revoked_at is None:
        session.revoked_at = timezone.now()
        session.save(update_fields=["revoked_at", "updated_at"])
    return session
