import pytest
from rest_framework import status

from spotseeker.user.tests.factories import UserFactory


@pytest.mark.django_db()
def test_bookmark_post(api_client, post):
    new_user = UserFactory()
    api_client.force_authenticate(user=new_user)
    response = api_client.post(
        f"/post/{post.id}/bookmark/",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
def test_unbookmark_post(api_client, post):
    new_user = UserFactory()
    api_client.force_authenticate(user=new_user)
    response = api_client.post(
        f"/post/{post.id}/bookmark/",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = api_client.post(
        f"/post/{post.id}/bookmark/",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
def test_post_is_bookmarked_by_user(api_client, post):
    new_user = UserFactory()
    api_client.force_authenticate(user=new_user)
    response = api_client.post(
        f"/post/{post.id}/bookmark/",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = api_client.get(f"/post/{post.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["is_bookmarked"] is True
