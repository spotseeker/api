import pytest
from rest_framework.test import APIClient

from spotseeker.post.models import Post
from spotseeker.post.tests.factories import PostFactory
from spotseeker.user.models import User
from spotseeker.user.tests.factories import UserFactory


@pytest.fixture()
def api_client() -> APIClient:
    """
    Fixture to provide an API client
    :return: APIClient
    """
    return APIClient()


@pytest.fixture()
def user(db) -> User:
    return UserFactory()


@pytest.fixture()
def post(db, user) -> Post:
    return PostFactory(user=user)
