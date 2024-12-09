import pytest
from rest_framework import status

from spotseeker.user.tests.factories import UserFactory


@pytest.mark.django_db()
def test_create_comment(api_client, post):
    new_user = UserFactory()
    api_client.force_authenticate(user=new_user)
    response = api_client.post(
        f"/post/{post.id}/comment/",
        {"comment": "test comment"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["comment"] == "test comment"
    assert response.data["user"]["id"] == str(new_user.id)


@pytest.mark.django_db()
def test_list_comments(api_client, post):
    new_user = UserFactory()
    api_client.force_authenticate(user=new_user)
    api_client.post(
        f"/post/{post.id}/comment/",
        {"comment": "test comment"},
    )
    response = api_client.get(f"/post/{post.id}/comment/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["comment"] == "test comment"
    assert response.data["results"][0]["user"]["id"] == str(new_user.id)


@pytest.mark.django_db()
def test_list_comments_other_user(api_client, post):
    new_user = UserFactory()
    api_client.force_authenticate(user=new_user)
    api_client.post(
        f"/post/{post.id}/comment/",
        {"comment": "test comment"},
    )
    api_client.force_authenticate(user=post.user)
    response = api_client.get(f"/post/{post.id}/comment/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["comment"] == "test comment"


@pytest.mark.django_db()
def test_update_comment(api_client, post):
    new_user = UserFactory()
    api_client.force_authenticate(user=new_user)
    response = api_client.post(
        f"/post/{post.id}/comment/",
        {"comment": "test comment"},
    )
    response = api_client.put(
        f"/post/{post.id}/comment/{response.data['id']}/",
        {"comment": "updated comment"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["comment"] == "updated comment"


@pytest.mark.django_db()
def test_delete_comment(api_client, post):
    api_client.force_authenticate(user=post.user)
    response = api_client.post(
        f"/post/{post.id}/comment/",
        {"comment": "test comment"},
    )
    response = api_client.delete(f"/post/{post.id}/comment/{response.data['id']}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = api_client.get(f"/post/{post.id}/comment/")
    assert response.data["count"] == 0
