from rest_framework import permissions


class IsOrganizationOwner(permissions.BasePermission):
    message = "You do not have permission to access this organization."

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        return obj.created_by_id == request.user.id
