from django.db import models

from config.models import BaseModel


class Location(BaseModel):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    code = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
