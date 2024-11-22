from django.urls import path
from rest_framework.routers import DefaultRouter

from spotseeker.user.views import NotificationView
from spotseeker.user.views import UserCreateView
from spotseeker.user.views import UserViewSet

router = DefaultRouter()

router.register("", UserViewSet)

app_name = "user"

urlpatterns = [
    path("", UserCreateView.as_view(), name="create"),
    *router.urls,
    path(
        "notification/",
        NotificationView.as_view({"get": "list"}),
        name="notification-list",
    ),
]
