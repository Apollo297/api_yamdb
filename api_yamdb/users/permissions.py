from rest_framework import permissions
from rest_framework.permissions import BasePermission


class AdminPermission(BasePermission):
    '''Разрешение наделяет правами Администратора.'''

    def has_permission(self, request, view):
        return request.user.is_admin


class IsAdminUserOrReadOnly(BasePermission):
    '''
    Разрешает только безопасные методы, наделяет правами Администратора.
    '''

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class AuthorOrHasRoleOrReadOnly(BasePermission):
    '''
    Разрешение проверяет имеет ли пользователь статус администратора,
    а также является ли он автором контента.
    '''

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )
