import googlemaps
from django.conf import settings
from rest_framework import serializers

from config.errors import ErrorMessages
from spotseeker.location.models import Location
from spotseeker.location.serializers import LocationDetailSerializer
from spotseeker.post.models import Post
from spotseeker.post.models import PostImage
from spotseeker.user.serializers.user import UserSerializer


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["media", "order"]


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(read_only=True)
    comments = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    is_bookmarked = serializers.BooleanField(read_only=True)
    images = PostImageSerializer(many=True)
    user = UserSerializer(read_only=True)
    location = LocationDetailSerializer(read_only=True)
    location_code = serializers.CharField(write_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["user", "deleted_at", "created_at", "updated_at"]
        extra_kwargs = {
            "location_code": {"write_only": True},
        }

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
        location_code = validated_data.pop("location_code")
        location = Location.objects.filter(code=location_code).first()
        if not location:
            gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
            try:
                results = gmaps.place(location_code, language="es-419")
            except googlemaps.exceptions.ApiError as e:
                raise serializers.ValidationError(ErrorMessages.INVALID_LOCATION) from e
            lat = results["result"]["geometry"]["location"]["lat"]
            lng = results["result"]["geometry"]["location"]["lng"]
            name = results["result"]["name"]
            location = Location.objects.create(
                code=location_code, name=name, latitude=lat, longitude=lng
            )
        post = Post.objects.create(location=location, **validated_data)
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
