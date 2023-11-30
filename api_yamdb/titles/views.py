from rest_framework import viewsets, mixins, permissions
from .models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .permissions import IsSuperUserIsAdminOrReadOnlyPermission


class CategoryCreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperUserIsAdminOrReadOnlyPermission,
    ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"


class GenreCreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperUserIsAdminOrReadOnlyPermission,
    ]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperUserIsAdminOrReadOnlyPermission,
    ]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
