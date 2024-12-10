import pytest
from rest_framework import status

from spotseeker.user.tests.factories import UserFactory


@pytest.mark.django_db()
def test_like_post(api_client, post):
    new_user = UserFactory()
    api_client.force_authenticate(user=new_user)
    response = api_client.post(
        f"/post/{post.id}/like/",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = api_client.get(f"/post/{post.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["likes"] == 1


@pytest.mark.django_db()
def test_unlike_post(api_client, post):
    new_user = UserFactory()
    api_client.force_authenticate(user=new_user)
    response = api_client.post(
        f"/post/{post.id}/like/",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = api_client.post(
        f"/post/{post.id}/like/",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = api_client.get(f"/post/{post.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["likes"] == 0


@pytest.mark.django_db()
def test_post_is_liked_by_user(api_client, post):
    new_user = UserFactory()
    api_client.force_authenticate(user=new_user)
    response = api_client.post(
        f"/post/{post.id}/like/",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = api_client.get(f"/post/{post.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["is_liked"] is True
