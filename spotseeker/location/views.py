import googlemaps
from django.conf import settings
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from spotseeker.location.serializers import LocationSerializer


class LocationView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LocationSerializer
    queryset = None

    def list(self, request, *args, **kwargs):
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        query = request.query_params.get("q")
        if not query:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        places = gmaps.places(query, language="es-419")
        serializer = self.get_serializer(data=places["results"], many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
