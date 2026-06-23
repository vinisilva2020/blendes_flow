from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.accounts.exceptions import AccountAlreadyExistsError, AccountInactiveError
from apps.authentication.models import AuthenticationSession

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

    return user


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
