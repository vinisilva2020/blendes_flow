from datetime import timedelta
from itertools import count

from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.authentication.models import AuthenticationSession, AuthenticationTokens


DEFAULT_PASSWORD = "StrongTestPassword123!"
_user_counter = count(1)


def create_user(**overrides):
    sequence = next(_user_counter)
    data = {
        "username": f"auth-user-{sequence}",
        "email": f"auth-user-{sequence}@example.com",
        "password": DEFAULT_PASSWORD,
        "is_active": True,
    }
    data.update(overrides)
    password = data.pop("password")
    return get_user_model().objects.create_user(password=password, **data)


def create_authentication_session(
    *,
    user=None,
    refresh_secret="refresh-secret",
    expires_at=None,
    revoked_at=None,
):
    user = user or create_user()
    expires_at = expires_at or timezone.now() + timedelta(days=1)
    return AuthenticationSession.objects.create(
        user=user,
        refresh_token_hash=AuthenticationTokens.hash_refresh_token(refresh_secret),
        expires_at=expires_at,
        revoked_at=revoked_at,
    )


def issue_access_token_for_user(user):
    refresh_secret = f"refresh-secret-{user.pk}"
    session = create_authentication_session(
        user=user,
        refresh_secret=refresh_secret,
    )
    return AuthenticationTokens.issue_authentication_tokens(
        session=session,
        refresh_secret=refresh_secret,
    ).access_token
