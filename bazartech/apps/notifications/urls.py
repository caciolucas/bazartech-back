from django.urls import path, include
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from rest_framework.routers import DefaultRouter

from notifications.views import test_notification

router = DefaultRouter()

router.register('devices', FCMDeviceAuthorizedViewSet)

urlpatterns = [
    # URLs will show up at <api_root>/devices
    # DRF browsable API which lists all available endpoints
    path('fcm/', include(router.urls)),
    path('test_notification/', test_notification)
]
