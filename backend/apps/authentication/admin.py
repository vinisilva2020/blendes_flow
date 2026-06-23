from django.contrib import admin

from apps.authentication.models import AuthenticationSession, SocialIdentity


@admin.register(AuthenticationSession)
class AuthenticationSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "revoked_at",
        "last_used_at",
        "expires_at",
        "created_at",
    )
    list_filter = ("revoked_at", "expires_at", "created_at")
    search_fields = ("id", "user__username", "user__email")
    readonly_fields = ("id", "refresh_token_hash", "created_at", "updated_at")


@admin.register(SocialIdentity)
class SocialIdentityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "provider",
        "provider_subject",
        "user",
        "email",
        "email_verified",
        "created_at",
    )
    list_filter = ("provider", "email_verified", "created_at")
    search_fields = ("provider_subject", "email", "user__username", "user__email")
    readonly_fields = ("created_at", "updated_at")
