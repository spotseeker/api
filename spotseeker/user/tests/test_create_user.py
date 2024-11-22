import pytest
from rest_framework import status

from spotseeker.user.tests.factories import UserFactory


@pytest.mark.django_db()
def test_create_user(api_client):
    user = UserFactory.build()
    response = api_client.post(
        "/user/",
        {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "birth_date": user.birth_date,
            "password": user.password,
        },
    )
    data = response.data
    assert response.status_code == status.HTTP_201_CREATED
    assert data["username"] == user.username


@pytest.mark.django_db()
def test_fail_username_exists(api_client):
    user = UserFactory()
    new_user = UserFactory.build(username=user.username)
    response = api_client.post(
        "/user/",
        {
            "username": user.username,
            "email": new_user.email,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "birth_date": new_user.birth_date,
            "password": new_user.password,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["username"][0] == "A user with that username already exists."


@pytest.mark.django_db()
def test_fail_email_exists(api_client):
    user = UserFactory()
    new_user = UserFactory.build(email=user.email)
    response = api_client.post(
        "/user/",
        {
            "username": new_user.username,
            "email": new_user.email,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "birth_date": new_user.birth_date,
            "password": new_user.password,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["email"][0] == "user with this email address already exists."
