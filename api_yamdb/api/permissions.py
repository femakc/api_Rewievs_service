from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """
    IsAdmin or Superuser permission .
    """
    def has_permission(self, request, view):
        return (
            request.user.role == 'admin'
            or request.user.is_superuser is True
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'admin'
            or request.user.is_superuser is True
        )
