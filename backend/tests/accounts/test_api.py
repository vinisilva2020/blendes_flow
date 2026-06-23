from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.common.throttles import RegistrationRateThrottle
from apps.authentication.models import AuthenticationSession
from tests.authentication.factories import (
    DEFAULT_PASSWORD,
    create_authentication_session,
    create_user,
    issue_access_token_for_user,
)


ACCOUNT_LIST_URL = "/api/v1/accounts/"
CURRENT_ACCOUNT_URL = "/api/v1/accounts/me/"


def account_registration_payload(**overrides):
    data = {
        "username": "api-account",
        "email": "api-account@example.com",
        "password": DEFAULT_PASSWORD,
        "password_confirm": DEFAULT_PASSWORD,
        "avatar_type": "gradient-blue",
    }
    data.update(overrides)
    return data


class AccountsAPITests(APITestCase):
    def setUp(self):
        cache.clear()

    def authenticate(self, user):
        token = issue_access_token_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_register_creates_account_without_exposing_passwords(self):
        response = self.client.post(
            ACCOUNT_LIST_URL,
            account_registration_payload(email="API.Account@Example.com"),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", response.data)
        self.assertNotIn("password_confirm", response.data)
        self.assertEqual(response.data["email"], "api.account@example.com")
        self.assertEqual(response.data["avatar_type"], "gradient-blue")

        user = get_user_model().objects.get(email="api.account@example.com")
        self.assertTrue(user.check_password(DEFAULT_PASSWORD))

    def test_register_rejects_missing_password_confirm(self):
        payload = account_registration_payload()
        payload.pop("password_confirm")

        response = self.client.post(ACCOUNT_LIST_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"]["code"], "validation_error")
        self.assertIn("password_confirm", response.data["error"]["details"])

    def test_register_rejects_mismatched_password_confirm(self):
        response = self.client.post(
            ACCOUNT_LIST_URL,
            account_registration_payload(password_confirm="DifferentPassword123!"),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"]["code"], "validation_error")
        self.assertIn("password_confirm", response.data["error"]["details"])

    def test_register_rejects_weak_password(self):
        response = self.client.post(
            ACCOUNT_LIST_URL,
            account_registration_payload(
                password="short",
                password_confirm="short",
            ),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"]["code"], "validation_error")
        self.assertIn("password", response.data["error"]["details"])

    def test_register_duplicate_account_returns_conflict(self):
        create_user(username="api-account", email="api-account@example.com")

        response = self.client.post(
            ACCOUNT_LIST_URL,
            account_registration_payload(),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["error"]["code"], "account_already_exists")

    def test_register_is_throttled(self):
        cache.clear()

        throttle_patch = patch.object(
            RegistrationRateThrottle,
            "rate",
            "2/minute",
            create=True,
        )
        throttle_patch.start()
        self.addCleanup(throttle_patch.stop)

        for index in range(2):
            response = self.client.post(
                ACCOUNT_LIST_URL,
                account_registration_payload(
                    username=f"throttle-user-{index}",
                    email=f"throttle-user-{index}@example.com",
                ),
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            ACCOUNT_LIST_URL,
            account_registration_payload(
                username="throttle-user-3",
                email="throttle-user-3@example.com",
            ),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertEqual(response.data["error"]["code"], "throttled")

    def test_me_requires_authentication(self):
        response = self.client.get(CURRENT_ACCOUNT_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"]["code"], "authentication_required")

    def test_me_returns_only_current_user_account(self):
        user = create_user(username="current-user", email="current-user@example.com")
        other_user = create_user(username="other-user", email="other-user@example.com")
        self.authenticate(user)

        response = self.client.get(CURRENT_ACCOUNT_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], user.id)
        self.assertNotEqual(response.data["id"], other_user.id)

    def test_patch_me_partially_updates_current_user_account(self):
        user = create_user(
            username="patch-user",
            email="patch-user@example.com",
            avatar_type="before",
        )
        self.authenticate(user)

        response = self.client.patch(
            CURRENT_ACCOUNT_URL,
            {
                "username": "patched-user",
                "email": "Patched.User@Example.com",
                "avatar_type": "after",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "patched-user")
        self.assertEqual(response.data["email"], "patched.user@example.com")
        self.assertEqual(response.data["avatar_type"], "after")

        user.refresh_from_db()
        self.assertEqual(user.username, "patched-user")
        self.assertEqual(user.email, "patched.user@example.com")
        self.assertEqual(user.avatar_type, "after")

    def test_patch_me_allows_empty_payload_without_changing_account(self):
        user = create_user(
            username="noop-user",
            email="noop-user@example.com",
            avatar_type="before",
        )
        self.authenticate(user)

        response = self.client.patch(CURRENT_ACCOUNT_URL, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "noop-user")
        self.assertEqual(response.data["email"], "noop-user@example.com")
        self.assertEqual(response.data["avatar_type"], "before")

    def test_patch_me_allows_clearing_avatar_type(self):
        user = create_user(
            username="clear-avatar-user",
            email="clear-avatar-user@example.com",
            avatar_type="before",
        )
        self.authenticate(user)

        response = self.client.patch(
            CURRENT_ACCOUNT_URL,
            {"avatar_type": None},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data["avatar_type"])

        user.refresh_from_db()
        self.assertIsNone(user.avatar_type)

    def test_patch_me_rejects_duplicate_account_data(self):
        create_user(username="taken-user", email="taken-user@example.com")
        user = create_user(username="patch-user", email="patch-user@example.com")
        self.authenticate(user)

        response = self.client.patch(
            CURRENT_ACCOUNT_URL,
            {"email": "taken-user@example.com"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["error"]["code"], "account_already_exists")

    def test_patch_me_requires_authentication(self):
        response = self.client.patch(
            CURRENT_ACCOUNT_URL,
            {"username": "anonymous-patch"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"]["code"], "authentication_required")

    def test_delete_me_soft_deletes_account_and_revokes_sessions(self):
        user = create_user(username="delete-user", email="delete-user@example.com")
        session = create_authentication_session(
            user=user,
            refresh_secret="session-to-revoke-on-delete",
        )
        self.authenticate(user)

        response = self.client.delete(CURRENT_ACCOUNT_URL)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        user.refresh_from_db()
        session.refresh_from_db()
        self.assertFalse(user.is_active)
        self.assertIsNotNone(session.revoked_at)
        self.assertFalse(
            AuthenticationSession.objects.filter(
                user=user,
                revoked_at__isnull=True,
            ).exists()
        )
