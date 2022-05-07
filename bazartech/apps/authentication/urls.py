from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework.routers import DefaultRouter

from django.urls import include, path

from authentication.views import RegisterView, UserViewSet

router = DefaultRouter()

router.register("users", UserViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="user_register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
]
