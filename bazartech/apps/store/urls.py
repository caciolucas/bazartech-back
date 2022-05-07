from store.views import ProductViewSet

from rest_framework.routers import DefaultRouter

from django.urls import include, path

router = DefaultRouter()

router.register("products", ProductViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
