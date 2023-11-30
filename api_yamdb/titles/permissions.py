from rest_framework import permissions


class IsSuperUserIsAdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff
                or request.user.is_superuser)