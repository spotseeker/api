from http import HTTPMethod

from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from config.serializers import ErrorSerializer
from spotseeker.user.models import Follow
from spotseeker.user.models import User
from spotseeker.user.models import UserOTP
from spotseeker.user.serializers import RecoverPasswordSerializer
from spotseeker.user.serializers import UserOTPSerializer
from spotseeker.user.serializers import UserPasswordUpdateSerializer
from spotseeker.user.serializers import UserProfileSerializer
from spotseeker.user.serializers import UserSerializer
from spotseeker.user.serializers import UserUpdateSerializer


class UserViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    @extend_schema(responses={200: UserSerializer})
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserProfileSerializer(instance)
        return Response(serializer.data)

    @extend_schema(
        request=UserUpdateSerializer, responses={200: UserSerializer, 403: None}
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = UserUpdateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = UserSerializer(user)
        return Response(response.data)

    @extend_schema(request=UserPasswordUpdateSerializer)
    @action(detail=True, methods=[HTTPMethod.POST])
    def follow(self, request, username):
        instance = self.get_object()
        follow, created = Follow.objects.get_or_create(
            follower_user=request.user, followed_user=instance
        )
        if not created:
            follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        request=UserOTPSerializer, responses={204: None, 400: ErrorSerializer}
    )
    @action(detail=False, methods=[HTTPMethod.POST])
    def otp(self, request):
        serializer = UserOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data["otp"]
        try:
            user_otp = UserOTP.objects.get(otp=otp, user=request.user)
        except UserOTP.DoesNotExist:
            data = ErrorSerializer({"error": "Invalid OTP"})
            return Response(data.data, status=status.HTTP_400_BAD_REQUEST)
        user_otp.delete()
        request.user.is_validated = True
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=UserPasswordUpdateSerializer)
    @action(detail=False, methods=[HTTPMethod.PATCH])
    def password(self, request):
        serializer = UserPasswordUpdateSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        password = make_password(serializer.validated_data["new_password"])
        request.user.password = password
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=RecoverPasswordSerializer)
    @action(detail=False, methods=[HTTPMethod.POST], url_path="password/reset")
    def recover_password(self, request):
        serializer = RecoverPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = make_password(serializer.validated_data["password"])
        request.user.password = password
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserFollowersView(GenericAPIView, ListModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @extend_schema(responses={200: UserSerializer})
    def get(self, request, username):
        user = get_object_or_404(
            User.objects.filter(deleted_at=None), username=username
        )
        followers = User.objects.filter(
            id__in=Follow.objects.filter(followed_user=user).values_list(
                "follower_user_id", flat=True
            )
        )
        page = self.paginate_queryset(followers)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data)


class UserFollowingView(GenericAPIView, ListModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @extend_schema(responses={200: UserSerializer})
    def get(self, request, username):
        user = get_object_or_404(
            User.objects.filter(deleted_at=None), username=username
        )
        following = User.objects.filter(
            id__in=Follow.objects.filter(follower_user=user).values_list(
                "followed_user_id", flat=True
            )
        )
        page = self.paginate_queryset(following)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(following, many=True)
        return Response(serializer.data)
