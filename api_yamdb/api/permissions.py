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


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False