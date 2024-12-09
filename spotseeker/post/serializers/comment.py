from rest_framework import serializers

from spotseeker.post.models import PostComment
from spotseeker.user.serializers.user import UserSerializer


class PostCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = ["id", "user", "comment"]
        read_only_fields = ["id", "user"]
