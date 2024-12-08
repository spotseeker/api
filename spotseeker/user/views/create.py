from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework.generics import CreateAPIView

from spotseeker.user.models import User
from spotseeker.user.models import UserOTP
from spotseeker.user.serializers import UserSerializer
from spotseeker.utils.email import EmailHelper


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        password = serializer.validated_data.pop("password")
        password = make_password(password)
        user = serializer.save(password=password)
        otp = UserOTP.objects.create(user=user)
        email = EmailHelper()
        email.send_onboarding_otp(user, otp.otp)
