from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from api.filters import TitleFilter
from api.mixins import SearchFieldsMixin
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)
from api.utils import (
    review_method,
    title_method
)
from reviews.models import (
    Category,
    Genre,
    Title,
)
from users.permissions import (
    AuthorOrHasRoleOrReadOnly,
    IsAdminUserOrReadOnly,
)


class CategoryViewSet(SearchFieldsMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(SearchFieldsMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    queryset = (Title.objects.annotate(
        rating=Avg(
            'reviews__score'
        )).all().order_by('-year')
    )
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete'
    ]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        AuthorOrHasRoleOrReadOnly
    )
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete'
    ]

    def get_queryset(self):
        return title_method(self.kwargs).reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=title_method(
                self.kwargs
            )
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        AuthorOrHasRoleOrReadOnly
    )
    http_method_names = [
        'patch',
        'get',
        'post',
        'delete'
    ]

    def get_queryset(self):
        return review_method(self.kwargs).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=review_method(
                self.kwargs
            )
        )
