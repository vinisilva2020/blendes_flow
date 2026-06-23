from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import User


@admin.register(User)
class AccountUserAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "avatar_type",
        "is_active",
        "is_staff",
        "date_joined",
    )
    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined")
    search_fields = ("email", "username")
    ordering = ("email",)
    fieldsets = UserAdmin.fieldsets + (
        ("Account profile", {"fields": ("avatar_type",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Account profile", {"fields": ("email", "avatar_type")}),
    )
