from rest_framework.routers import DefaultRouter

from django.urls import include, path

from common.views import CityViewSet

router = DefaultRouter()

router.register("cities", CityViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
