from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.common.throttles import RegistrationRateThrottle
from apps.authentication.exceptions import InvalidGoogleCredentialError
from apps.authentication.models import AuthenticationSession, SocialIdentity
from tests.authentication.factories import (
    DEFAULT_PASSWORD,
    create_authentication_session,
    create_social_identity,
    create_user,
    issue_access_token_for_user,
)


ACCOUNT_LIST_URL = "/api/v1/accounts/"
CURRENT_ACCOUNT_URL = "/api/v1/accounts/me/"
CURRENT_ACCOUNT_GOOGLE_SOCIAL_ACCOUNT_URL = (
    "/api/v1/accounts/me/social-accounts/google/"
)
CURRENT_ACCOUNT_PASSWORD_URL = "/api/v1/accounts/me/password/"


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

    def test_me_returns_linked_social_accounts(self):
        user = create_user(username="social-user", email="social-user@example.com")
        create_social_identity(
            user=user,
            provider_subject="profile-google-subject",
            email="social-user@gmail.com",
        )
        self.authenticate(user)

        response = self.client.get(CURRENT_ACCOUNT_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["social_accounts"],
            [
                {
                    "provider": "google",
                    "email": "social-user@gmail.com",
                    "email_verified": True,
                    "can_unlink": True,
                    "created_at": response.data["social_accounts"][0]["created_at"],
                    "updated_at": response.data["social_accounts"][0]["updated_at"],
                }
            ],
        )
        self.assertNotIn("provider_subject", response.data["social_accounts"][0])

    def test_me_marks_only_google_login_as_not_unlinkable(self):
        user = create_user(username="google-only-profile", email="google-only@example.com")
        user.set_unusable_password()
        user.save(update_fields=["password"])
        create_social_identity(
            user=user,
            provider_subject="google-only-profile-subject",
            email="google-only@gmail.com",
        )
        self.authenticate(user)

        response = self.client.get(CURRENT_ACCOUNT_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["social_accounts"][0]["can_unlink"])

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

    def test_delete_google_social_account_unlinks_current_user_identity(self):
        user = create_user(username="unlink-user", email="unlink-user@example.com")
        create_social_identity(
            user=user,
            provider_subject="unlink-google-subject",
            email="unlink-user@gmail.com",
        )
        self.authenticate(user)

        response = self.client.delete(CURRENT_ACCOUNT_GOOGLE_SOCIAL_ACCOUNT_URL)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            SocialIdentity.objects.filter(
                user=user,
                provider="google",
            ).exists()
        )

    def test_post_google_social_account_links_current_user_identity(self):
        user = create_user(username="link-user", email="link-user@example.com")
        self.authenticate(user)
        claims = {
            "sub": "link-google-subject",
            "email": "link-user@gmail.com",
            "email_verified": True,
        }

        with patch(
            "apps.accounts.services.verify_google_id_token",
            return_value=claims,
        ):
            response = self.client.post(
                CURRENT_ACCOUNT_GOOGLE_SOCIAL_ACCOUNT_URL,
                {"credential": "google-credential"},
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            SocialIdentity.objects.filter(
                user=user,
                provider="google",
                provider_subject="link-google-subject",
                email="link-user@gmail.com",
            ).exists()
        )
        self.assertEqual(response.data["social_accounts"][0]["provider"], "google")

    def test_post_google_social_account_updates_current_user_existing_identity(self):
        user = create_user(username="relink-user", email="relink-user@example.com")
        create_social_identity(
            user=user,
            provider_subject="relink-google-subject",
            email="old-google@example.com",
        )
        self.authenticate(user)
        claims = {
            "sub": "relink-google-subject",
            "email": "new-google@example.com",
            "email_verified": True,
        }

        with patch(
            "apps.accounts.services.verify_google_id_token",
            return_value=claims,
        ):
            response = self.client.post(
                CURRENT_ACCOUNT_GOOGLE_SOCIAL_ACCOUNT_URL,
                {"credential": "google-credential"},
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        identity = SocialIdentity.objects.get(provider_subject="relink-google-subject")
        self.assertEqual(identity.user, user)
        self.assertEqual(identity.email, "new-google@example.com")

    def test_post_google_social_account_rejects_identity_linked_to_other_user(self):
        owner = create_user(username="google-owner", email="google-owner@example.com")
        user = create_user(username="google-linker", email="google-linker@example.com")
        create_social_identity(
            user=owner,
            provider_subject="taken-google-subject",
            email="owner-google@example.com",
        )
        self.authenticate(user)
        claims = {
            "sub": "taken-google-subject",
            "email": "owner-google@example.com",
            "email_verified": True,
        }

        with patch(
            "apps.accounts.services.verify_google_id_token",
            return_value=claims,
        ):
            response = self.client.post(
                CURRENT_ACCOUNT_GOOGLE_SOCIAL_ACCOUNT_URL,
                {"credential": "google-credential"},
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["error"]["code"], "social_account_conflict")

    def test_post_google_social_account_rejects_email_owned_by_other_user(self):
        create_user(username="email-owner", email="google-email@example.com")
        user = create_user(username="email-linker", email="email-linker@example.com")
        self.authenticate(user)
        claims = {
            "sub": "new-google-subject",
            "email": "google-email@example.com",
            "email_verified": True,
        }

        with patch(
            "apps.accounts.services.verify_google_id_token",
            return_value=claims,
        ):
            response = self.client.post(
                CURRENT_ACCOUNT_GOOGLE_SOCIAL_ACCOUNT_URL,
                {"credential": "google-credential"},
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["error"]["code"], "social_account_conflict")

    def test_post_google_social_account_rejects_invalid_credential(self):
        user = create_user(username="bad-google-link", email="bad-google-link@example.com")
        self.authenticate(user)

        with patch(
            "apps.accounts.services.verify_google_id_token",
            side_effect=InvalidGoogleCredentialError,
        ):
            response = self.client.post(
                CURRENT_ACCOUNT_GOOGLE_SOCIAL_ACCOUNT_URL,
                {"credential": "bad-google-credential"},
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["error"]["code"],
            "invalid_social_account_credential",
        )

    def test_delete_google_social_account_rejects_missing_identity(self):
        user = create_user(username="missing-social", email="missing-social@example.com")
        self.authenticate(user)

        response = self.client.delete(CURRENT_ACCOUNT_GOOGLE_SOCIAL_ACCOUNT_URL)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"]["code"], "social_account_not_found")

    def test_delete_google_social_account_preserves_last_login_method(self):
        user = create_user(username="google-only", email="google-only@example.com")
        user.set_unusable_password()
        user.save(update_fields=["password"])
        create_social_identity(
            user=user,
            provider_subject="last-google-subject",
            email="google-only@gmail.com",
        )
        self.authenticate(user)

        response = self.client.delete(CURRENT_ACCOUNT_GOOGLE_SOCIAL_ACCOUNT_URL)

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["error"]["code"], "last_authentication_method")
        self.assertTrue(
            SocialIdentity.objects.filter(
                user=user,
                provider="google",
            ).exists()
        )

    def test_delete_google_social_account_requires_authentication(self):
        response = self.client.delete(CURRENT_ACCOUNT_GOOGLE_SOCIAL_ACCOUNT_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"]["code"], "authentication_required")

    def test_put_password_sets_local_password_for_social_only_account(self):
        user = create_user(username="set-password", email="set-password@example.com")
        user.set_unusable_password()
        user.save(update_fields=["password"])
        create_social_identity(
            user=user,
            provider_subject="set-password-google-subject",
            email="set-password@gmail.com",
        )
        self.authenticate(user)

        response = self.client.put(
            CURRENT_ACCOUNT_PASSWORD_URL,
            {
                "new_password": "NewStrongPassword123!",
                "password_confirm": "NewStrongPassword123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        user.refresh_from_db()
        self.assertTrue(user.check_password("NewStrongPassword123!"))

    def test_put_password_requires_current_password_for_local_account(self):
        user = create_user(username="change-password", email="change-password@example.com")
        self.authenticate(user)

        response = self.client.put(
            CURRENT_ACCOUNT_PASSWORD_URL,
            {
                "new_password": "NewStrongPassword123!",
                "password_confirm": "NewStrongPassword123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"]["code"], "validation_error")
        self.assertIn("current_password", response.data["error"]["details"])

    def test_put_password_rejects_invalid_current_password(self):
        user = create_user(username="bad-current", email="bad-current@example.com")
        self.authenticate(user)

        response = self.client.put(
            CURRENT_ACCOUNT_PASSWORD_URL,
            {
                "current_password": "wrong-password",
                "new_password": "NewStrongPassword123!",
                "password_confirm": "NewStrongPassword123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"]["code"], "invalid_current_password")

    def test_put_password_changes_local_password_with_current_password(self):
        user = create_user(username="good-current", email="good-current@example.com")
        self.authenticate(user)

        response = self.client.put(
            CURRENT_ACCOUNT_PASSWORD_URL,
            {
                "current_password": DEFAULT_PASSWORD,
                "new_password": "NewStrongPassword123!",
                "password_confirm": "NewStrongPassword123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        user.refresh_from_db()
        self.assertTrue(user.check_password("NewStrongPassword123!"))

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
