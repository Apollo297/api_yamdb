from rest_framework import (
    mixins,
    viewsets
)
from rest_framework.filters import SearchFilter

from users.permissions import IsAdminUserOrReadOnly


class SearchFieldsMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
