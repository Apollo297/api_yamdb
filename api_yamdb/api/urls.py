from django.urls import include, path

from users.views import (
    CreateUserViewSet,
    GetTokenViewSet,
)

from rest_framework import routers
router = routers.DefaultRouter()
router.register('auth/signup', CreateUserViewSet, basename='signup')
router.register('auth/token', GetTokenViewSet, basename='gettoken')


urlpatterns = [
    path('v1/', include(router.urls)),
]
