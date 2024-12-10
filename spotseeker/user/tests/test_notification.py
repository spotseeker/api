import pytest
from rest_framework import status

from spotseeker.user.tests.factories import UserFactory


@pytest.mark.django_db()
def test_notification_user_follow(api_client, user):
    new_user = UserFactory()
    api_client.force_authenticate(user=user)
    response = api_client.post(f"/user/{new_user.username}/follow/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    api_client.force_authenticate(user=new_user)
    response = api_client.get(f"/user/{new_user.username}/notification/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert (
        response.data["results"][0]["content"] == f"{user.username} empezó a seguirte"
    )


@pytest.mark.django_db()
def test_notification_user_post_like(api_client, post):
    new_user = UserFactory()
    api_client.force_authenticate(user=new_user)
    response = api_client.post(f"/post/{post.id}/like/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    api_client.force_authenticate(user=post.user)
    response = api_client.get(f"/user/{post.user.username}/notification/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert (
        response.data["results"][0]["content"]
        == f"{new_user.username} le gustó tu publicación"
    )


@pytest.mark.django_db()
def test_notification_user_post_comment(api_client, post):
    new_user = UserFactory()
    api_client.force_authenticate(user=new_user)
    response = api_client.post(f"/post/{post.id}/comment/", {"comment": "test comment"})
    assert response.status_code == status.HTTP_201_CREATED
    api_client.force_authenticate(user=post.user)
    response = api_client.get(f"/user/{post.user.username}/notification/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert (
        response.data["results"][0]["content"]
        == f"{new_user.username} comentó tu publicación"
    )
