import pytest
from model_bakery import baker
from rest_framework import status


@pytest.mark.django_db()
def test_send_otp(api_client, mocker):
    user = baker.make("user.User")
    mocker.patch(
        "spotseeker.user.views.password.EmailHelper.send_password_reset_otp",
        return_value=None,
    )
    response = api_client.post(
        "/user/password/recover/",
        {"email": user.email},
    )
    otp = user.userotp_set.first()
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert otp is not None


@pytest.mark.django_db()
def test_send_otp_invalid_email(api_client, mocker):
    user = baker.make("user.User")
    mocker.patch(
        "spotseeker.user.views.password.EmailHelper.send_password_reset_otp",
        return_value=None,
    )
    response = api_client.post(
        "/user/password/recover/",
        {"email": "a" + user.email},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.userotp_set.count() == 0


@pytest.mark.django_db()
def test_send_otp_twice(api_client, mocker):
    user = baker.make("user.User")
    mocker.patch(
        "spotseeker.user.views.password.EmailHelper.send_password_reset_otp",
        return_value=None,
    )
    response = api_client.post(
        "/user/password/recover/",
        {"email": user.email},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = api_client.post(
        "/user/password/recover/",
        {"email": user.email},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.userotp_set.count() == 1


@pytest.mark.django_db()
def test_validate_otp(api_client, mocker):
    user = baker.make("user.User")
    otp = baker.make("user.UserOTP", user=user)
    response = api_client.post(
        "/user/password/recover/otp/",
        {"otp": otp.otp},
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


@pytest.mark.django_db()
def test_validate_otp_invalid_otp(api_client):
    response = api_client.post(
        "/user/password/recover/otp/",
        {"otp": "123456"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "Invalid OTP"


@pytest.mark.django_db()
def test_validate_otp_no_otp(api_client):
    response = api_client.post(
        "/user/password/recover/otp/",
        {"otp": "123456"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "Invalid OTP"


@pytest.mark.django_db()
def test_reset_password(api_client):
    user = baker.make("user.User")
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/user/password/reset/",
        {"password": "newpassword"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    user.refresh_from_db()
    assert user.check_password("newpassword")
