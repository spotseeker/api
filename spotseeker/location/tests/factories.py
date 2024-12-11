from factory import Faker
from factory.django import DjangoModelFactory

from spotseeker.location.models import Location


class LocationFactory(DjangoModelFactory):
    name = Faker("city")
    latitude = Faker("latitude")
    longitude = Faker("longitude")
    code = Faker("pystr")

    class Meta:
        model = Location
