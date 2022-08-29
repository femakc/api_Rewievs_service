from rest_framework import permissions

class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if request.method in permissions.SAFE_METHODS or request.user.role == 'admin':
                return True
        except:
            return False
