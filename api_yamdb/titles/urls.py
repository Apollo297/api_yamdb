from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import (
    TitleViewSet,
    CategoryCreateListDestroyViewSet,
    GenreCreateListDestroyViewSet,
)

router = DefaultRouter()
router.register("categories", CategoryCreateListDestroyViewSet, basename="categories")
router.register("genres", GenreCreateListDestroyViewSet, basename="genres")
router.register("titles", TitleViewSet, basename="title")

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include("djoser.urls.jwt")),
]
