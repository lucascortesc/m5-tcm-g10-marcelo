import uuid

from django.core.validators import MinValueValidator
from django.db import models


class Room(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    number = models.CharField(max_length=15)
    number_of_beds = models.PositiveIntegerField()
    is_vacant = models.BooleanField(default=True)
    capacity = models.PositiveIntegerField()
    description = models.TextField()
    rent_price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
        )
    floor = models.CharField(max_length=100)

    hotel = models.ForeignKey(
        "hotels.Hotel", on_delete=models.CASCADE, related_name="rooms"
    )


class RoomAmenity(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50)

    room = models.ManyToManyField("rooms.Room", related_name="amenities")
