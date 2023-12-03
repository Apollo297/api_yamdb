from rest_framework.permissions import BasePermission

from api_yamdb.settings import (
    ADMIN,
)


class AdminPermission(BasePermission):
    '''Разрешение наделяет правами Администратора.'''

    def has_permission(self, request, view):
        return (
            request.user.role == ADMIN
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == ADMIN
            or request.user.is_staff
        )
