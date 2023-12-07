from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import (
    mixins,
    viewsets
)
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from api.filters import TitleFilter
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    ReviewSerializer,
    CommentSerializer,
)
from api.utils import title_method
from reviews.models import (
    Category,
    Genre,
    Review,
    Title
)
from users.permissions import (
    AuthorOrHasRoleOrReadOnly,
    IsAdminUserOrReadOnly,
)


class SearchFieldsMixin:
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(
    SearchFieldsMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter,)


class GenreViewSet(
    SearchFieldsMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter,)


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
            title=title_method(self.kwargs)
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
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review,
            id=review_id,
            title=title_method(self.kwargs)
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review,
            id=review_id,
            title=title_method(self.kwargs)
        )
        serializer.save(
            author=self.request.user,
            review=review
        )
