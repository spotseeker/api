from rest_framework import serializers


class LocationSerializer(serializers.Serializer):
    name = serializers.CharField()
    place_id = serializers.CharField()


class LocationSearchSerializer(serializers.Serializer):
    q = serializers.CharField()
