from django.urls import path

from spotseeker.user.views import NotificationView
from spotseeker.user.views import RecoverPasswordOTPView
from spotseeker.user.views import RecoverPasswordView
from spotseeker.user.views import UserCreateView
from spotseeker.user.views import UserFollowersView
from spotseeker.user.views import UserFollowingView
from spotseeker.user.views import UserViewSet

app_name = "user"

urlpatterns = [
    path("", UserCreateView.as_view(), name="create"),
    path(
        "<str:username>/",
        UserViewSet.as_view({"get": "retrieve", "patch": "partial_update"}),
        name="user-detail",
    ),
    path("<str:username>/otp/", UserViewSet.as_view({"post": "otp"}), name="user-otp"),
    path(
        "<str:username>/follow/",
        UserViewSet.as_view({"post": "follow"}),
        name="user-follow",
    ),
    path(
        "<str:username>/password/",
        UserViewSet.as_view({"patch": "password", "post": "password"}),
        name="user-password",
    ),
    path("<str:username>/followers/", UserFollowersView.as_view(), name="followers"),
    path("<str:username>/following/", UserFollowingView.as_view(), name="followers"),
    path(
        "<str:username>/notification/",
        NotificationView.as_view(),
        name="notification-list",
    ),
    path("password/recover/", RecoverPasswordView.as_view(), name="recover-password"),
    path(
        "password/recover/otp/",
        RecoverPasswordOTPView.as_view(),
        name="recover-password-otp",
    ),
]
