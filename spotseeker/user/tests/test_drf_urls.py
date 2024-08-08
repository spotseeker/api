from django.urls import resolve
from django.urls import reverse

from spotseeker.user.models import User


def test_user_detail(user: User):
    assert (
        reverse("user:user-detail", kwargs={"username": user.username})
        == f"/user/{user.username}/"
    )
    assert resolve(f"/user/{user.username}/").view_name == "user:user-detail"


def test_user_list():
    assert reverse("user:user-list") == "/user/"
    assert resolve("/user/").view_name == "user:user-list"


def test_user_me():
    assert reverse("user:user-me") == "/user/me/"
    assert resolve("/user/me/").view_name == "user:user-me"
