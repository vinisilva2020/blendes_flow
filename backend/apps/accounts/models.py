from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models.functions import Lower


class AccountUserManager(UserManager):
    """Manager that uses email as the authentication identifier."""

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email must be set.")

        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user account authenticated by email."""

    email = models.EmailField(unique=True)
    avatar_type = models.CharField(max_length=64, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = AccountUserManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("email"),
                name="unique_account_user_email_ci",
            ),
        ]
        indexes = [
            models.Index(fields=["email"], name="account_user_email_idx"),
        ]

    def __str__(self):
        return self.email
