from rest_framework import serializers

from spotseeker.post.models import PostComment


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ["user", "comment"]
        read_only_fields = ["user"]
