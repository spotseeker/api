from django.urls import path
from rest_framework.routers import DefaultRouter

from spotseeker.user.views import NotificationView
from spotseeker.user.views import RecoverPasswordOTPView
from spotseeker.user.views import RecoverPasswordView
from spotseeker.user.views import UserCreateView
from spotseeker.user.views import UserViewSet
from spotseeker.user.views.user import UserFollowersView
from spotseeker.user.views.user import UserFollowingView

router = DefaultRouter()

router.register("", UserViewSet)

app_name = "user"

urlpatterns = [
    path("", UserCreateView.as_view(), name="create"),
    *router.urls,
    path("<str:username>/followers/", UserFollowersView.as_view(), name="followers"),
    path("<str:username>/following/", UserFollowingView.as_view(), name="followers"),
    path(
        "notification/",
        NotificationView.as_view({"get": "list"}),
        name="notification-list",
    ),
    path("password/recover/", RecoverPasswordView.as_view(), name="recover-password"),
    path(
        "password/recover/otp/",
        RecoverPasswordOTPView.as_view(),
        name="recover-password-otp",
    ),
]
