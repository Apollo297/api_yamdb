from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)
from users.views import (
    CreateUserViewSet,
    GetTokenViewSet,
    SignUpUserViewSet,
)

app_name = 'api'

router = DefaultRouter()

router.register(
    'categories',
    CategoryViewSet,
    basename='сategories',
)
router.register(
    'titles',
    TitleViewSet,
    basename='titles',
)
router.register(
    'genres',
    GenreViewSet,
    basename='genres',
)
router.register(
    'auth/signup',
    SignUpUserViewSet,
    basename='signup',
)
router.register(
    'auth/token',
    GetTokenViewSet,
    basename='gettoken',
)
router.register(
    'users',
    CreateUserViewSet,
    basename='users',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review-list'
)

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment-list'
)


urlpatterns = [
    path('v1/', include(router.urls)),
]
