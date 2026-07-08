from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import IntegrityError, transaction
from django.db.models import Prefetch
from django.utils import timezone

from apps.accounts.exceptions import (
    AccountAlreadyExistsError,
    AccountInactiveError,
    InvalidSocialAccountCredentialError,
    InvalidCurrentPasswordError,
    LastAuthenticationMethodError,
    SocialAccountConflictError,
    SocialAccountHostedDomainError,
    SocialAccountNotFoundError,
    UnverifiedSocialAccountEmailError,
)
from apps.authentication.exceptions import (
    GoogleAuthenticationNotConfiguredError,
    InvalidGoogleCredentialError,
)
from apps.authentication.models import (
    AuthenticationSession,
    SocialIdentity,
    SocialIdentityProvider,
)
from apps.authentication.services import verify_google_id_token

UNSET = object()


@transaction.atomic
def create_account_service(*, username, email, password, avatar_type=None):
    """Create a local account with a hashed password."""
    user_model = get_user_model()
    email = email.strip().lower()

    if user_model.objects.filter(email__iexact=email).exists():
        raise AccountAlreadyExistsError
    if user_model.objects.filter(username=username).exists():
        raise AccountAlreadyExistsError

    try:
        return user_model.objects.create_user(
            username=username,
            email=email,
            password=password,
            avatar_type=avatar_type,
        )
    except IntegrityError:
        raise AccountAlreadyExistsError


def get_current_account_service(user):
    """Return the authenticated user's account."""
    if not user.is_active:
        raise AccountInactiveError

    social_identities = SocialIdentity.objects.only(
        "provider",
        "email",
        "email_verified",
        "created_at",
        "updated_at",
        "user_id",
    ).order_by("provider")
    return (
        get_user_model()
        .objects.prefetch_related(
            Prefetch(
                "social_identities",
                queryset=social_identities,
                to_attr="prefetched_social_identities",
            )
        )
        .get(pk=user.pk)
    )


@transaction.atomic
def update_current_account_service(
    user,
    username=UNSET,
    email=UNSET,
    avatar_type=UNSET,
):
    """Partially update the authenticated user's account."""
    if not user.is_active:
        raise AccountInactiveError

    user_model = get_user_model()
    update_fields = []

    if username is not UNSET and username != user.username:
        if user_model.objects.filter(username=username).exclude(pk=user.pk).exists():
            raise AccountAlreadyExistsError

        user.username = username
        update_fields.append("username")

    if email is not UNSET:
        email = email.strip().lower()
        if email != user.email:
            if (
                user_model.objects.filter(email__iexact=email)
                .exclude(pk=user.pk)
                .exists()
            ):
                raise AccountAlreadyExistsError

            user.email = email
            update_fields.append("email")

    if avatar_type is not UNSET and avatar_type != user.avatar_type:
        user.avatar_type = avatar_type
        update_fields.append("avatar_type")

    if not update_fields:
        return user

    try:
        user.full_clean()
        user.save(update_fields=update_fields)
    except IntegrityError:
        raise AccountAlreadyExistsError

    return user


@transaction.atomic
def update_current_account_password_service(
    user,
    *,
    new_password,
    current_password=UNSET,
):
    """Set or change the authenticated user's local password."""
    if not user.is_active:
        raise AccountInactiveError

    if user.has_usable_password():
        if current_password is UNSET or not user.check_password(current_password):
            raise InvalidCurrentPasswordError

    user.set_password(new_password)
    user.full_clean()
    user.save(update_fields=["password"])
    return user


@transaction.atomic
def link_current_google_social_account_service(user, credential):
    """Link a verified Google identity to the authenticated user."""
    if not user.is_active:
        raise AccountInactiveError

    try:
        claims = verify_google_id_token(credential)
    except (
        GoogleAuthenticationNotConfiguredError,
        InvalidGoogleCredentialError,
    ):
        raise InvalidSocialAccountCredentialError

    provider_subject = claims.get("sub")
    email = (claims.get("email") or "").strip().lower()
    email_verified_claim = claims.get("email_verified")
    email_verified = (
        email_verified_claim is True
        or str(email_verified_claim).lower() == "true"
    )

    if not provider_subject:
        raise InvalidSocialAccountCredentialError
    if not email or not email_verified:
        raise UnverifiedSocialAccountEmailError

    allowed_hosted_domain = settings.GOOGLE_ALLOWED_HOSTED_DOMAIN
    if allowed_hosted_domain and claims.get("hd") != allowed_hosted_domain:
        raise SocialAccountHostedDomainError

    identity = (
        SocialIdentity.objects.select_for_update()
        .filter(
            provider=SocialIdentityProvider.GOOGLE,
            provider_subject=provider_subject,
        )
        .first()
    )
    if identity is not None and identity.user_id != user.pk:
        raise SocialAccountConflictError

    user_model = get_user_model()
    if user_model.objects.filter(email__iexact=email).exclude(pk=user.pk).exists():
        raise SocialAccountConflictError

    if identity is None:
        identity = SocialIdentity.objects.create(
            provider=SocialIdentityProvider.GOOGLE,
            provider_subject=provider_subject,
            user=user,
            email=email,
            email_verified=email_verified,
        )
        return identity

    if identity.email != email or identity.email_verified != email_verified:
        identity.email = email
        identity.email_verified = email_verified
        identity.save(update_fields=["email", "email_verified", "updated_at"])

    return identity


@transaction.atomic
def unlink_current_social_account_service(user, provider):
    """Remove a linked social account from the authenticated user."""
    if not user.is_active:
        raise AccountInactiveError

    if provider not in SocialIdentityProvider.values:
        raise SocialAccountNotFoundError

    identity = (
        SocialIdentity.objects.select_for_update()
        .filter(user=user, provider=provider)
        .first()
    )
    if identity is None:
        raise SocialAccountNotFoundError

    linked_identity_count = (
        SocialIdentity.objects.select_for_update()
        .filter(user=user)
        .count()
    )
    if not user.has_usable_password() and linked_identity_count <= 1:
        raise LastAuthenticationMethodError

    identity.delete()
    return None


@transaction.atomic
def delete_current_account_service(user):
    """Soft-delete an account and revoke all active sessions."""
    if not user.is_active:
        return user

    now = timezone.now()
    user.is_active = False
    user.save(update_fields=["is_active"])
    AuthenticationSession.objects.filter(
        user=user,
        revoked_at__isnull=True,
    ).update(revoked_at=now, updated_at=now)
    return user
