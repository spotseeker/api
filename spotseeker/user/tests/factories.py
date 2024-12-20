from collections.abc import Sequence
from typing import Any

from factory import Faker
from factory import SubFactory
from factory import post_generation
from factory.django import DjangoModelFactory

from spotseeker.user.models import Follow
from spotseeker.user.models import User
from spotseeker.user.models import UserOTP


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    birth_date = "2000-01-01"

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):  # noqa: FBT001
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = User
        django_get_or_create = ["username"]


class UserOTPFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)

    class Meta:
        model = UserOTP


class FollowFactory(DjangoModelFactory):
    follower_user = SubFactory(UserFactory)
    followed_user = SubFactory(UserFactory)

    class Meta:
        model = Follow
