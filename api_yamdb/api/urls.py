from django.urls import include, path
from rest_framework import routers

from users.views import (
    CreateUserViewSet,
    GetTokenViewSet,
    SignUpUserViewSet,
)

router = routers.DefaultRouter()
router.register('auth/signup', SignUpUserViewSet, basename='signup')
router.register('auth/token', GetTokenViewSet, basename='gettoken')
router.register('users', CreateUserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router.urls)),
]
