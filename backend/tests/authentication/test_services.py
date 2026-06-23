from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.utils import timezone

from apps.authentication.exceptions import (
    AuthenticationSessionNotFoundError,
    GoogleAccountConflictError,
    GoogleAccountHostedDomainError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    UnverifiedGoogleEmailError,
)
from apps.authentication.models import (
    AuthenticationSession,
    AuthenticationTokens,
    SocialIdentity,
    SocialIdentityProvider,
)
from apps.authentication.services import (
    authenticate_google_user_service,
    authenticate_user_service,
    refresh_authentication_session_service,
    revoke_authentication_session_service,
)
from tests.authentication.factories import (
    DEFAULT_PASSWORD,
    create_authentication_session,
    create_social_identity,
    create_user,
)


class AuthenticateUserServiceTests(TestCase):
    def test_authenticate_user_creates_session_and_returns_tokens(self):
        user = create_user(username="login-user")

        tokens = authenticate_user_service(user.email, DEFAULT_PASSWORD)

        session = AuthenticationSession.objects.get(id=tokens.session_id)
        parsed_refresh_token = AuthenticationTokens.parse_refresh_token(
            tokens.refresh_token,
        )

        self.assertEqual(session.user, user)
        self.assertTrue(session.is_active)
        self.assertEqual(tokens.token_type, "Bearer")
        self.assertEqual(parsed_refresh_token[0], session.id)
        self.assertNotEqual(session.refresh_token_hash, parsed_refresh_token[1])

    def test_authenticate_user_rejects_invalid_credentials(self):
        create_user(username="login-user", email="login-user@example.com")

        with self.assertRaises(InvalidCredentialsError):
            authenticate_user_service("login-user@example.com", "wrong-password")

    def test_authenticate_user_rejects_inactive_user(self):
        user = create_user(username="inactive-user", is_active=False)

        with self.assertRaises(InvalidCredentialsError):
            authenticate_user_service(user.email, DEFAULT_PASSWORD)


@override_settings(GOOGLE_OAUTH_CLIENT_ID="google-client-id")
class AuthenticateGoogleUserServiceTests(TestCase):
    def test_authenticate_google_user_creates_user_identity_and_session(self):
        claims = {
            "sub": "google-subject-1",
            "email": "Google.User@Example.com",
            "email_verified": True,
            "given_name": "Google",
            "family_name": "User",
        }

        with patch(
            "apps.authentication.services.verify_google_id_token",
            return_value=claims,
        ):
            tokens = authenticate_google_user_service("credential")

        session = AuthenticationSession.objects.get(id=tokens.session_id)
        identity = SocialIdentity.objects.get(
            provider=SocialIdentityProvider.GOOGLE,
            provider_subject="google-subject-1",
        )

        self.assertEqual(session.user, identity.user)
        self.assertTrue(session.is_active)
        self.assertEqual(identity.email, "google.user@example.com")
        self.assertTrue(identity.email_verified)
        self.assertEqual(tokens.token_type, "Bearer")

    def test_authenticate_google_user_reuses_existing_social_identity(self):
        user = create_user(email="old@example.com")
        create_social_identity(
            user=user,
            provider_subject="google-subject-2",
            email="old@example.com",
        )
        claims = {
            "sub": "google-subject-2",
            "email": "new@example.com",
            "email_verified": True,
        }

        with patch(
            "apps.authentication.services.verify_google_id_token",
            return_value=claims,
        ):
            tokens = authenticate_google_user_service("credential")

        session = AuthenticationSession.objects.get(id=tokens.session_id)
        identity = SocialIdentity.objects.get(provider_subject="google-subject-2")

        self.assertEqual(session.user, user)
        self.assertEqual(identity.email, "new@example.com")

    def test_authenticate_google_user_rejects_existing_local_email(self):
        create_user(email="existing@example.com")
        claims = {
            "sub": "google-subject-3",
            "email": "existing@example.com",
            "email_verified": True,
        }

        with patch(
            "apps.authentication.services.verify_google_id_token",
            return_value=claims,
        ):
            with self.assertRaises(GoogleAccountConflictError):
                authenticate_google_user_service("credential")

    def test_authenticate_google_user_rejects_unverified_email(self):
        claims = {
            "sub": "google-subject-4",
            "email": "unverified@example.com",
            "email_verified": False,
        }

        with patch(
            "apps.authentication.services.verify_google_id_token",
            return_value=claims,
        ):
            with self.assertRaises(UnverifiedGoogleEmailError):
                authenticate_google_user_service("credential")

    @override_settings(GOOGLE_ALLOWED_HOSTED_DOMAIN="example.com")
    def test_authenticate_google_user_rejects_unallowed_hosted_domain(self):
        claims = {
            "sub": "google-subject-5",
            "email": "user@other.example",
            "email_verified": True,
            "hd": "other.example",
        }

        with patch(
            "apps.authentication.services.verify_google_id_token",
            return_value=claims,
        ):
            with self.assertRaises(GoogleAccountHostedDomainError):
                authenticate_google_user_service("credential")


class RefreshAuthenticationSessionServiceTests(TestCase):
    def test_refresh_session_rotates_refresh_secret_and_updates_last_used_at(self):
        session = create_authentication_session(refresh_secret="old-secret")
        old_hash = session.refresh_token_hash
        refresh_token = AuthenticationTokens.build_refresh_token(
            session_id=session.id,
            secret="old-secret",
        )

        tokens = refresh_authentication_session_service(refresh_token)

        session.refresh_from_db()
        self.assertEqual(tokens.session_id, session.id)
        self.assertNotEqual(session.refresh_token_hash, old_hash)
        self.assertIsNotNone(session.last_used_at)

    def test_refresh_session_rejects_reused_refresh_token(self):
        session = create_authentication_session(refresh_secret="old-secret")
        refresh_token = AuthenticationTokens.build_refresh_token(
            session_id=session.id,
            secret="old-secret",
        )

        refresh_authentication_session_service(refresh_token)

        with self.assertRaises(InvalidRefreshTokenError):
            refresh_authentication_session_service(refresh_token)

    def test_refresh_session_rejects_revoked_session(self):
        session = create_authentication_session(
            refresh_secret="secret",
            revoked_at=timezone.now(),
        )
        refresh_token = AuthenticationTokens.build_refresh_token(
            session_id=session.id,
            secret="secret",
        )

        with self.assertRaises(InvalidRefreshTokenError):
            refresh_authentication_session_service(refresh_token)

    def test_refresh_session_rejects_expired_session(self):
        session = create_authentication_session(
            refresh_secret="secret",
            expires_at=timezone.now() - timedelta(seconds=1),
        )
        refresh_token = AuthenticationTokens.build_refresh_token(
            session_id=session.id,
            secret="secret",
        )

        with self.assertRaises(InvalidRefreshTokenError):
            refresh_authentication_session_service(refresh_token)


class RevokeAuthenticationSessionServiceTests(TestCase):
    def test_revoke_session_sets_revoked_at_for_owned_session(self):
        user = create_user(username="owner")
        session = create_authentication_session(user=user)

        result = revoke_authentication_session_service(session.id, user.id)

        session.refresh_from_db()
        self.assertEqual(result, session)
        self.assertIsNotNone(session.revoked_at)

    def test_revoke_session_is_scoped_to_user(self):
        owner = create_user(username="owner")
        other_user = create_user(username="other-user")
        session = create_authentication_session(user=owner)

        result = revoke_authentication_session_service(session.id, other_user.id)

        session.refresh_from_db()
        self.assertIs(result, AuthenticationSessionNotFoundError)
        self.assertIsNone(session.revoked_at)
