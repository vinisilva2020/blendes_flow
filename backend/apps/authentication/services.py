import re
import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from django.utils import timezone
from google.auth.exceptions import GoogleAuthError
from google.oauth2 import id_token as google_id_token

from apps.authentication.exceptions import (
    AuthenticationSessionNotFoundError,
    GoogleAccountConflictError,
    GoogleAccountHostedDomainError,
    GoogleAuthenticationNotConfiguredError,
    InvalidCredentialsError,
    InvalidGoogleCredentialError,
    InvalidRefreshTokenError,
    UnverifiedGoogleEmailError,
)
from apps.authentication.models import (
    AuthenticationSession,
    AuthenticationTokens,
    SocialIdentity,
    SocialIdentityProvider,
)


def issue_authentication_session_tokens_for_user(user):
    """Cria uma sessao revogavel e emite tokens internos para o usuario."""
    refresh_secret = AuthenticationTokens.generate_refresh_secret()
    session = AuthenticationSession.objects.create(
        user=user,
        refresh_token_hash=AuthenticationTokens.hash_refresh_token(refresh_secret),
        expires_at=timezone.now()
        + timedelta(seconds=settings.AUTH_SESSION_LIFETIME_SECONDS),
    )
    return AuthenticationTokens.issue_authentication_tokens(
        session=session,
        refresh_secret=refresh_secret,
    )


def authenticate_user_service(identifier, password):
    """Autentica um usuario com base no identificador e senha fornecidos."""
    user = authenticate(username=identifier.strip().lower(), password=password)
    if user is None or not user.is_active:
        raise InvalidCredentialsError

    return issue_authentication_session_tokens_for_user(user)


def verify_google_id_token(credential):
    """Valida um ID token do Google e retorna suas claims."""
    if not settings.GOOGLE_OAUTH_CLIENT_ID:
        raise GoogleAuthenticationNotConfiguredError

    try:
        from google.auth.transport import requests as google_auth_requests

        return google_id_token.verify_oauth2_token(
            credential,
            google_auth_requests.Request(),
            settings.GOOGLE_OAUTH_CLIENT_ID,
        )
    except (GoogleAuthError, ImportError, ValueError):
        raise InvalidGoogleCredentialError


@transaction.atomic
def authenticate_google_user_service(credential):
    """Autentica ou cadastra um usuario a partir de uma credencial Google."""
    claims = verify_google_id_token(credential)
    provider_subject = claims.get("sub")
    email = (claims.get("email") or "").strip().lower()
    email_verified_claim = claims.get("email_verified")
    email_verified = (
        email_verified_claim is True
        or str(email_verified_claim).lower() == "true"
    )
    allowed_hosted_domain = settings.GOOGLE_ALLOWED_HOSTED_DOMAIN

    if not provider_subject:
        raise InvalidGoogleCredentialError
    if not email or not email_verified:
        raise UnverifiedGoogleEmailError
    if allowed_hosted_domain and claims.get("hd") != allowed_hosted_domain:
        raise GoogleAccountHostedDomainError

    identity = (
        SocialIdentity.objects.select_for_update()
        .select_related("user")
        .filter(
            provider=SocialIdentityProvider.GOOGLE,
            provider_subject=provider_subject,
        )
        .first()
    )
    if identity is not None:
        if not identity.user.is_active:
            raise InvalidCredentialsError

        if identity.email != email or identity.email_verified != email_verified:
            identity.email = email
            identity.email_verified = email_verified
            identity.save(update_fields=["email", "email_verified", "updated_at"])

        return issue_authentication_session_tokens_for_user(identity.user)

    user_model = get_user_model()
    if user_model.objects.filter(email__iexact=email).exists():
        raise GoogleAccountConflictError

    user = create_google_user_from_claims(claims=claims, email=email)
    SocialIdentity.objects.create(
        provider=SocialIdentityProvider.GOOGLE,
        provider_subject=provider_subject,
        user=user,
        email=email,
        email_verified=email_verified,
    )

    return issue_authentication_session_tokens_for_user(user)


def create_google_user_from_claims(*, claims, email):
    """Cria um usuario local para uma identidade Google validada."""
    user_model = get_user_model()
    user_data = {}
    model_fields = {field.name for field in user_model._meta.fields}

    if "email" in model_fields:
        user_data["email"] = email
    if "username" in model_fields:
        user_data["username"] = generate_google_username(
            email=email,
            provider_subject=claims["sub"],
            user_model=user_model,
        )
    if "first_name" in model_fields:
        user_data["first_name"] = claims.get("given_name", "")[:150]
    if "last_name" in model_fields:
        user_data["last_name"] = claims.get("family_name", "")[:150]

    user = user_model(**user_data)
    user.set_unusable_password()
    user.save()
    return user


def generate_google_username(*, email, provider_subject, user_model):
    """Gera um username unico e estavel a partir dos dados do Google."""
    username_field = user_model._meta.get_field("username")
    max_length = username_field.max_length or 150
    local_part = email.split("@", maxsplit=1)[0]
    base = re.sub(r"[^A-Za-z0-9_.+-]", "", local_part) or "google-user"
    suffix = provider_subject[:8]

    for counter in range(10):
        counter_suffix = f"-{suffix}" if counter == 0 else f"-{suffix}-{counter}"
        candidate = f"{base[: max_length - len(counter_suffix)]}{counter_suffix}"
        if not user_model.objects.filter(username=candidate).exists():
            return candidate

    fallback_suffix = secrets.token_urlsafe(8).replace("-", "").replace("_", "")
    counter_suffix = f"-{fallback_suffix}"
    return f"{base[: max_length - len(counter_suffix)]}{counter_suffix}"


@transaction.atomic
def refresh_authentication_session_service(refresh_token):
    """Renova uma sessao de autenticacao utilizando um token de atualizacao."""
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
        session=session,
        refresh_secret=new_refresh_secret,
    )


@transaction.atomic
def revoke_authentication_session_service(session_id, user_id):
    """Revoga de forma idempotente uma sessao pertencente ao usuario autenticado."""
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
