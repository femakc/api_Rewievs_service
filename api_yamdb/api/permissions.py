from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """
    IsAdmin or Superuser permission .
    """
    def has_permission(self, request, view):
        print(request.user)
        return (
            request.user.role == 'admin'
            or request.user.is_superuser is True
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'admin'
            or request.user.is_superuser is True
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
        