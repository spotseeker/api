import pytest
from rest_framework import status

from config.errors import ErrorMessages
from spotseeker.user.tests.factories import UserFactory


@pytest.mark.django_db()
def test_update_user_bio(api_client, user):
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        f"/user/{user.username}/",
        {"description": "Hello, world!"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["description"] == "Hello, world!"


@pytest.mark.django_db()
def test_update_user_names(api_client, user):
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        f"/user/{user.username}/",
        {"first_name": "John", "last_name": "Doe"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == "John"
    assert response.data["last_name"] == "Doe"


@pytest.mark.django_db()
def test_update_user_names_empty(api_client, user):
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        f"/user/{user.username}/",
        {"first_name": "", "last_name": ""},
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db()
def test_update_password(api_client):
    user = UserFactory(password="password")  # noqa: S106
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        "/user/password/",
        {"password": "password", "new_password": "new_password"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.check_password("new_password")


@pytest.mark.django_db()
def test_update_password_wrong_password(api_client):
    user = UserFactory(password="password")  # noqa: S106
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        "/user/password/",
        {"password": "wrong_password", "new_password": "new_password"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.data
    assert response.data["password"][0] == ErrorMessages.INVALID_PASSWORD
