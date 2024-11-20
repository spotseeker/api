from rest_framework import serializers

from spotseeker.post.models import Post
from spotseeker.post.models import PostComment
from spotseeker.post.models import PostImage


class PostImage(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["media", "order"]


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(read_only=True)
    comments = serializers.IntegerField(read_only=True)
    images = serializers.ListField(child=PostImage())

    class Meta:
        model = Post
        fields = "__all__"


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["body", "is_archived", "score"]


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ["user", "comment"]
