"""pdt URL Configuration."""

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path(
        "auth/token/",
        TokenObtainPairView.as_view(),
        name="api.auth.obtain_jwt_token",
    ),
    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="api.auth.refresh_jwt_token",
    ),
    path(
        "auth/token/verify/",
        TokenVerifyView.as_view(),
        name="api.auth.verify_jwt_token",
    ),
]
