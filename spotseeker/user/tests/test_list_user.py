import pytest
from rest_framework import status

from spotseeker.user.tests.factories import UserFactory


@pytest.mark.django_db()
def test_username_not_available(api_client, user):
    response = api_client.get(f"/user/?username={user.username}")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] is True


@pytest.mark.django_db()
def test_email_not_available(api_client, user):
    response = api_client.get(f"/user/?email={user.email}")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] is True


@pytest.mark.django_db()
def test_username_available(api_client, user):
    response = api_client.get(f"/user/?username={user.username[:-1]}")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] is False


@pytest.mark.django_db()
def test_email_available(api_client, user):
    other_user = UserFactory.build()
    response = api_client.get(f"/user/?email={other_user.email}")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] is False


@pytest.mark.django_db()
def test_username_and_email_available(api_client):
    user = UserFactory.build()
    response = api_client.get(f"/user/?username={user.username}&email={user.email}")
    assert response.data["username"] is False
    assert response.data["email"] is False


@pytest.mark.django_db()
def test_availability_bad_request(api_client):
    response = api_client.get("/user/")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
