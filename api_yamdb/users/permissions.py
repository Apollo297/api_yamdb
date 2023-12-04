from rest_framework.permissions import BasePermission
from rest_framework import permissions

from api_yamdb.settings import ADMIN


class AdminPermission(BasePermission):
    '''Разрешение наделяет правами Администратора.'''

    def has_permission(self, request, view):
        return (request.user.role == ADMIN or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return (request.user.role == ADMIN or request.user.is_staff)


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == ADMIN
        return False


class AuthorOrHasRoleOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'superuser'
            or request.user.role == 'admin'
            or request.user.role == 'moderator'
            or obj.author == request.user
        )
