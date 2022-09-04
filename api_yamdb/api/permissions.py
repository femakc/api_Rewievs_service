from rest_framework import permissions

from api_yamdb.settings import ADMIN, MODERATOR


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission .
    """
    def has_permission(self, request, view):
        return (
            request.user.is_staff
            or request.user.is_authenticated
        )


class IsAdminRole(permissions.BasePermission):
    """
    IsAdmin or Superuser permission .
    """
    def has_permission(self, request, view):
        return (
            request.user.role == ADMIN
            or request.user.is_superuser
        )


class IsOwnerPatch(permissions.BasePermission):
    """
    Только владелец.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method == "PATCH"
            or obj.author == request.user
        )


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        else:
            return (
                request.method in permissions.SAFE_METHODS
                or request.user.role == ADMIN
            )


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Кастомное разрешение,
    только автор имеет право на редактирование."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == ADMIN
            or request.user.role == MODERATOR
        )
