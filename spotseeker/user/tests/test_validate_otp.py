import pytest
from model_bakery import baker
from rest_framework import status


@pytest.mark.django_db()
def test_validate_otp(api_client):
    user = baker.make("user.User")
    otp = baker.make("user.UserOTP", user=user)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/user/otp/",
        {"otp": otp.otp},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
def test_invalid_otp(api_client):
    user = baker.make("user.User")
    baker.make("user.UserOTP", user=user, otp="234568")
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/user/otp/",
        {"otp": "123456"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "Invalid OTP"
