from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, ListViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"lists", ListViewSet, basename="list")

urlpatterns = [
    path("", include(router.urls)),
]
