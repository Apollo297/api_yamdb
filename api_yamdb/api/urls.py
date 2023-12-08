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
    GetToken,
    SignUpUser,
)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories',
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles',
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres',
)
router_v1.register(
    'users',
    CreateUserViewSet,
    basename='users',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

registration_patterns = [
    path('auth/signup/', SignUpUser.as_view(), name='signup'),
    path('auth/token/', GetToken.as_view(), name='gettoken'),
]

include_patterns = [
    path('', include(router_v1.urls)),
    path('', include(registration_patterns)),
]

urlpatterns = [
    path('v1/', include(include_patterns))
]
