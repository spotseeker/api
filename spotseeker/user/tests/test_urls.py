from django.urls import resolve
from django.urls import reverse

from spotseeker.user.models import User


def test_user_detail(user: User):
    assert (
        reverse("user:user-detail", kwargs={"username": user.username})
        == f"/user/{user.username}/"
    )
    assert resolve(f"/user/{user.username}/").view_name == "user:user-detail"


def test_create_user():
    assert reverse("user:create") == "/user/"


def test_user_otp(user: User):
    assert (
        reverse("user:user-otp", kwargs={"username": user.username})
        == f"/user/{user.username}/otp/"
    )


def test_user_password(user: User):
    assert (
        reverse("user:user-password", kwargs={"username": user.username})
        == f"/user/{user.username}/password/"
    )


def test_user_notification(user: User):
    assert (
        reverse("user:notification-list", kwargs={"username": user.username})
        == f"/user/{user.username}/notification/"
    )
