import pytest
from rest_framework import status

from spotseeker.user.tests.factories import FollowFactory
from spotseeker.user.tests.factories import UserFactory


@pytest.mark.django_db()
def test_followers(api_client, user):
    new_user = UserFactory()
    FollowFactory(followed_user=user, follower_user=new_user)
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/user/{user.username}/followers/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["username"] == new_user.username


@pytest.mark.django_db()
def test_followers_other_user(api_client, user):
    new_user = UserFactory()
    FollowFactory(followed_user=new_user, follower_user=user)
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/user/{new_user.username}/followers/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1


@pytest.mark.django_db()
def test_following(api_client, user):
    new_user = UserFactory()
    FollowFactory(followed_user=new_user, follower_user=user)
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/user/{user.username}/following/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["username"] == new_user.username


@pytest.mark.django_db()
def test_following_other_user(api_client, user):
    new_user = UserFactory()
    FollowFactory(followed_user=user, follower_user=new_user)
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/user/{new_user.username}/following/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1


@pytest.mark.django_db()
def test_follow_user(api_client, user):
    new_user = UserFactory()
    api_client.force_authenticate(user=user)
    response = api_client.post(f"/user/{new_user.username}/follow/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
def test_unfollow_user(api_client, user):
    new_user = UserFactory()
    FollowFactory(followed_user=new_user, follower_user=user)
    api_client.force_authenticate(user=user)
    response = api_client.post(f"/user/{new_user.username}/follow/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
def test_follow_user_invalid(api_client, user):
    api_client.force_authenticate(user=user)
    response = api_client.post("/user/invalid/follow/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
