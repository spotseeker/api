from rest_framework import serializers

from spotseeker.location.models import Location


class LocationSerializer(serializers.Serializer):
    name = serializers.CharField()
    place_id = serializers.CharField()


class LocationSearchSerializer(serializers.Serializer):
    q = serializers.CharField()


class LocationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
