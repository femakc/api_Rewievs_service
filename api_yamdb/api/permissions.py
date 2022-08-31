from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission .
    """
    def has_permission(self, request, view):
        return (
            request.user.is_staff
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):

        if request.method == 'PATH' or obj.username == request.user:
            print('PATH user=request user')
            return True

        return request.user.is_staff
        # return (
        #     request.method in permissions.SAFE_METHODS
        #     or obj.author == request.user
        # )


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


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == 'admin'
        return False


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
            or request.user.role == 'admin'
            or request.user.role == 'moderator'
        )
