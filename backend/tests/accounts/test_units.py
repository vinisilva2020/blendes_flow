from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from tests.authentication.factories import DEFAULT_PASSWORD


class AccountUserModelTests(TestCase):
    def test_create_user_normalizes_email(self):
        user = get_user_model().objects.create_user(
            username="unit-user",
            email="Unit.User@Example.COM",
            password=DEFAULT_PASSWORD,
        )

        self.assertEqual(user.email, "unit.user@example.com")
        self.assertTrue(user.check_password(DEFAULT_PASSWORD))

    def test_create_user_requires_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                username="unit-user",
                email="",
                password=DEFAULT_PASSWORD,
            )

    def test_create_user_requires_username(self):
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                email="unit-user@example.com",
                password=DEFAULT_PASSWORD,
            )

    def test_avatar_type_accepts_null_blank_and_string(self):
        user_model = get_user_model()
        null_avatar = user_model.objects.create_user(
            username="null-avatar",
            email="null-avatar@example.com",
            password=DEFAULT_PASSWORD,
            avatar_type=None,
        )
        blank_avatar = user_model.objects.create_user(
            username="blank-avatar",
            email="blank-avatar@example.com",
            password=DEFAULT_PASSWORD,
            avatar_type="",
        )
        string_avatar = user_model.objects.create_user(
            username="string-avatar",
            email="string-avatar@example.com",
            password=DEFAULT_PASSWORD,
            avatar_type="gradient-blue",
        )

        self.assertIsNone(null_avatar.avatar_type)
        self.assertEqual(blank_avatar.avatar_type, "")
        self.assertEqual(string_avatar.avatar_type, "gradient-blue")

    def test_email_uniqueness_is_case_insensitive(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            username="case-user",
            email="Case.User@Example.com",
            password=DEFAULT_PASSWORD,
        )

        with self.assertRaises(ValidationError):
            user_model.objects.create_user(
                username="case-user-2",
                email="case.user@example.com",
                password=DEFAULT_PASSWORD,
            )
