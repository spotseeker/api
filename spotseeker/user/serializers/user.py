from rest_framework import serializers

from config.errors import ErrorMessages
from spotseeker.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "password",
            "description",
            "avatar",
            "is_validated",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "deleted_at": {"read_only": True},
            "is_validated": {"read_only": True},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    followers = serializers.IntegerField(source="followers.count", read_only=True)
    following = serializers.IntegerField(source="following.count", read_only=True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "description",
            "avatar",
            "is_validated",
            "created_at",
            "updated_at",
            "deleted_at",
            "followers",
            "following",
            "is_following",
        ]

    def get_is_following(self, obj):
        user = self.context["request"].user
        return user.following.filter(followed_user_id=obj.pk).exists()


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "birth_date",
            "description",
            "avatar",
        ]


class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField()

    class Meta:
        model = User
        fields = ["password", "new_password"]

    def validate_password(self, value):
        user = self.instance
        if not user.check_password(value):
            raise serializers.ValidationError(ErrorMessages.INVALID_PASSWORD)
        return value


class RecoverPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()


class UserAvailableSearchSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()


class UserAvailableSerializer(serializers.Serializer):
    username = serializers.BooleanField()
    email = serializers.BooleanField()
