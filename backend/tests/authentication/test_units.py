from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.authentication.api.v1.serializers import (
    AuthenticationSessionOutputSerializerV1,
)
from apps.authentication.models import AuthenticationTokens
from tests.authentication.factories import create_authentication_session, create_user


class AuthenticationTokensUnitTests(TestCase):
    def test_refresh_token_roundtrip(self):
        session = create_authentication_session()
        refresh_token = AuthenticationTokens.build_refresh_token(
            session_id=session.id,
            secret="plain-secret",
        )

        parsed = AuthenticationTokens.parse_refresh_token(refresh_token)

        self.assertEqual(parsed, (session.id, "plain-secret"))

    def test_invalid_refresh_token_returns_none(self):
        invalid_values = [
            "",
            "not-a-token",
            "not-a-uuid.secret",
            None,
        ]

        for value in invalid_values:
            with self.subTest(value=value):
                self.assertIsNone(AuthenticationTokens.parse_refresh_token(value))

    def test_hash_refresh_token_is_deterministic_and_does_not_store_secret(self):
        secret = "plain-secret"

        token_hash = AuthenticationTokens.hash_refresh_token(secret)

        self.assertEqual(token_hash, AuthenticationTokens.hash_refresh_token(secret))
        self.assertNotEqual(token_hash, secret)
        self.assertEqual(len(token_hash), 64)


class AuthenticationSessionUnitTests(TestCase):
    def test_session_is_active_when_not_revoked_and_not_expired(self):
        session = create_authentication_session()

        self.assertFalse(session.is_revoked)
        self.assertFalse(session.is_expired)
        self.assertTrue(session.is_active)

    def test_session_is_inactive_when_expired(self):
        session = create_authentication_session(
            expires_at=timezone.now() - timedelta(seconds=1),
        )

        self.assertTrue(session.is_expired)
        self.assertFalse(session.is_active)

    def test_session_serializer_marks_current_session(self):
        user = create_user(username="serializer-user")
        current_session = create_authentication_session(user=user)
        other_session = create_authentication_session(
            user=user,
            refresh_secret="other-secret",
        )

        serializer = AuthenticationSessionOutputSerializerV1(
            [current_session, other_session],
            many=True,
            context={"current_session_id": str(current_session.id)},
        )

        self.assertTrue(serializer.data[0]["is_current"])
        self.assertFalse(serializer.data[1]["is_current"])
