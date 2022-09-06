import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Hotel(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14, unique=True)
    stars = models.PositiveIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    address = models.OneToOneField(
        "addresses.Address", on_delete=models.CASCADE, related_name="hotel"
    )


class Amenity(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    hotel = models.ManyToManyField(Hotel, related_name="amenities")
