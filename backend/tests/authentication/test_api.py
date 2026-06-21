from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.authentication.models import AuthenticationSession
from tests.authentication.factories import (
    DEFAULT_PASSWORD,
    create_authentication_session,
    create_user,
)


@override_settings(ROOT_URLCONF="tests.authentication.urls")
class AuthenticationAPITests(APITestCase):
    def test_login_returns_tokens_and_creates_session(self):
        user = create_user(username="api-login-user")

        response = self.client.post(
            reverse("login"),
            {
                "identifier": user.username,
                "password": DEFAULT_PASSWORD,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)
        self.assertEqual(response.data["token_type"], "Bearer")
        self.assertTrue(
            AuthenticationSession.objects.filter(
                id=response.data["session_id"],
                user=user,
                revoked_at__isnull=True,
            ).exists()
        )

    def test_login_rejects_invalid_credentials(self):
        create_user(username="api-login-user")

        response = self.client.post(
            reverse("login"),
            {
                "identifier": "api-login-user",
                "password": "wrong-password",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"]["code"], "invalid_credentials")

    def test_refresh_returns_rotated_refresh_token(self):
        user = create_user(username="api-refresh-user")
        login_response = self.client.post(
            reverse("login"),
            {
                "identifier": user.username,
                "password": DEFAULT_PASSWORD,
            },
            format="json",
        )

        response = self.client.post(
            reverse("refresh"),
            {
                "refresh_token": login_response.data["refresh_token"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(
            response.data["refresh_token"],
            login_response.data["refresh_token"],
        )
        self.assertEqual(response.data["session_id"], login_response.data["session_id"])

    def test_logout_revokes_current_session(self):
        user = create_user(username="api-logout-user")
        login_response = self.client.post(
            reverse("login"),
            {
                "identifier": user.username,
                "password": DEFAULT_PASSWORD,
            },
            format="json",
        )
        access_token = login_response.data["access_token"]
        session_id = login_response.data["session_id"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.post(reverse("logout"), format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        session = AuthenticationSession.objects.get(id=session_id)
        self.assertIsNotNone(session.revoked_at)

    def test_session_list_requires_authentication(self):
        response = self.client.get(reverse("session-list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"]["code"], "authentication_required")

    def test_session_list_returns_only_active_sessions_for_current_user(self):
        user = create_user(username="api-session-list-user")
        other_user = create_user(username="api-other-user")
        login_response = self.client.post(
            reverse("login"),
            {
                "identifier": user.username,
                "password": DEFAULT_PASSWORD,
            },
            format="json",
        )
        active_session = AuthenticationSession.objects.get(
            id=login_response.data["session_id"],
        )
        create_authentication_session(
            user=user,
            refresh_secret="revoked-secret",
            revoked_at=active_session.created_at,
        )
        create_authentication_session(user=other_user, refresh_secret="other-secret")

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login_response.data['access_token']}",
        )
        response = self.client.get(reverse("session-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], str(active_session.id))
        self.assertTrue(response.data[0]["is_current"])

    def test_revoke_session_revokes_owned_session(self):
        user = create_user(username="api-revoke-user")
        login_response = self.client.post(
            reverse("login"),
            {
                "identifier": user.username,
                "password": DEFAULT_PASSWORD,
            },
            format="json",
        )
        session = create_authentication_session(
            user=user,
            refresh_secret="session-to-revoke",
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login_response.data['access_token']}",
        )
        response = self.client.delete(reverse("session-revoke", args=[session.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        session.refresh_from_db()
        self.assertIsNotNone(session.revoked_at)

    def test_refresh_rejects_invalid_token(self):
        response = self.client.post(
            reverse("refresh"),
            {"refresh_token": "invalid-token"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"]["code"], "invalid_refresh_token")

    def test_access_token_is_rejected_after_session_revocation(self):
        user = create_user(username="api-revoked-access-user")
        login_response = self.client.post(
            reverse("login"),
            {
                "identifier": user.username,
                "password": DEFAULT_PASSWORD,
            },
            format="json",
        )
        session = AuthenticationSession.objects.get(
            id=login_response.data["session_id"],
        )
        session.revoked_at = session.created_at
        session.save(update_fields=["revoked_at", "updated_at"])

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login_response.data['access_token']}",
        )
        response = self.client.get(reverse("session-list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"]["code"], "invalid_access_token")
