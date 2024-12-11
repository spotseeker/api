from spotseeker.location.models import Location


def populate_location():
    location, _ = Location.objects.get_or_create(
        code="ChIJhy6EDu1mh44R37_kP7jWUJc",
        name="Obelisco de Barquisimeto",
        latitude=10.067064626793913,
        longitude=-69.35620677523828,
    )
    return location.id
