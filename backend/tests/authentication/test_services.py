from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.authentication.exceptions import (
    AuthenticationSessionNotFoundError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
)
from apps.authentication.models import AuthenticationSession, AuthenticationTokens
from apps.authentication.services import (
    authenticate_user_service,
    refresh_authentication_session_service,
    revoke_authentication_session_service,
)
from tests.authentication.factories import (
    DEFAULT_PASSWORD,
    create_authentication_session,
    create_user,
)


class AuthenticateUserServiceTests(TestCase):
    def test_authenticate_user_creates_session_and_returns_tokens(self):
        user = create_user(username="login-user")

        tokens = authenticate_user_service(user.username, DEFAULT_PASSWORD)

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
        create_user(username="login-user")

        with self.assertRaises(InvalidCredentialsError):
            authenticate_user_service("login-user", "wrong-password")

    def test_authenticate_user_rejects_inactive_user(self):
        create_user(username="inactive-user", is_active=False)

        with self.assertRaises(InvalidCredentialsError):
            authenticate_user_service("inactive-user", DEFAULT_PASSWORD)


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
