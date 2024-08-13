import pytest

from spotseeker.user.models import User
from spotseeker.user.tests.factories import UserFactory


@pytest.fixture()
def user(db) -> User:
    return UserFactory()
