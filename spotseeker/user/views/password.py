from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from config.serializers import ErrorSerializer
from spotseeker.user.models import User
from spotseeker.user.models import UserOTP
from spotseeker.user.serializers import EmailSerializer
from spotseeker.user.serializers import UserOTPSerializer
from spotseeker.utils.email import EmailHelper


class RecoverPasswordView(APIView):
    @extend_schema(request=EmailSerializer, responses={204: None})
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email, deleted_at__isnull=True)
        except User.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        otp, _ = UserOTP.objects.get_or_create(user=user)
        email = EmailHelper()
        email.send_password_reset_otp(user, otp.otp)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecoverPasswordOTPView(APIView):
    @extend_schema(
        request=UserOTPSerializer,
        responses={200: TokenObtainPairSerializer, 400: ErrorSerializer},
    )
    @transaction.atomic
    def post(self, request):
        serializer = UserOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data["otp"]
        try:
            user_otp = UserOTP.objects.get(otp=otp)
        except UserOTP.DoesNotExist:
            data = ErrorSerializer({"error": "Invalid OTP"})
            return Response(data.data, status=status.HTTP_400_BAD_REQUEST)
        user_otp.delete()
        refresh = RefreshToken.for_user(user_otp.user)
        return Response(
            {"refresh": str(refresh), "access": str(refresh.access_token)},
            status=status.HTTP_200_OK,
        )
