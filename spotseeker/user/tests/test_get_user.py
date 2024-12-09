import pytest
from rest_framework import status

from spotseeker.user.tests.factories import FollowFactory
from spotseeker.user.tests.factories import UserFactory


@pytest.mark.django_db()
def test_get_own_user(api_client, user):
    other_user = UserFactory()
    FollowFactory(follower_user=user, followed_user=other_user)
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/user/{user.username}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == str(user.id)
    assert response.data["username"] == user.username
    assert response.data["email"] == user.email
    assert response.data["followers"] == 0
    assert response.data["following"] == 1
    assert response.data["is_following"] is False


@pytest.mark.django_db()
def test_other_user(api_client, user):
    other_user = UserFactory()
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/user/{other_user.username}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == other_user.username
    assert response.data["is_following"] is False


@pytest.mark.django_db()
def test_other_user_following(api_client, user):
    other_user = UserFactory()
    FollowFactory(follower_user=user, followed_user=other_user)
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/user/{other_user.username}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == other_user.username
    assert response.data["is_following"] is True
