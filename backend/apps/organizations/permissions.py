from rest_framework import permissions

from apps.organizations.models import OrganizationMembership, Role


class IsOrganizationMemberReadOnlyOrAdminOwnerWrite(permissions.BasePermission):
    message = "You do not have permission to modify this organization."

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        role = getattr(obj, "_current_user_membership_role", None)
        if role is None:
            role = (
                OrganizationMembership.objects.filter(
                    user=request.user,
                    organization=obj,
                )
                .values_list("role", flat=True)
                .first()
            )

        if role is None:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return role in (Role.OWNER, Role.ADMIN)
