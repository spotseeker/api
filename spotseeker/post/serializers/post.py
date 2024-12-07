from django.conf import settings
from rest_framework import serializers

from config.errors import ErrorMessages
from spotseeker.post.models import Post
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

    def validate_images(self, images):
        count = len(images)
        if count == 0:
            raise serializers.ValidationError(ErrorMessages.NO_IMAGES)
        if count > settings.MAX_IMAGES_PER_POST:
            raise serializers.ValidationError(ErrorMessages.MAX_IMAGES)
        if count != len({image["order"] for image in images}):
            raise serializers.ValidationError(ErrorMessages.UNIQUE_IMAGES_ORDER)
        return images

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
