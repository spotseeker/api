from rest_framework import serializers

from spotseeker.post.models import Post
from spotseeker.post.models import PostComment
from spotseeker.post.models import PostImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["media", "order"]


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(read_only=True)
    comments = serializers.IntegerField(read_only=True)
    images = PostImageSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["user", "deleted_at", "created_at", "updated_at"]

    def create(self, validated_data):
        images = validated_data.pop("images")
        post = Post.objects.create(**validated_data)
        created_images = [
            PostImage.objects.create(
                post=post, media=image["media"], order=image["order"]
            )
            for image in images
        ]
        post.images = created_images
        return post


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["body", "is_archived", "score"]


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ["user", "comment"]
