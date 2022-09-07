from django.db import models
import uuid


class Room(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    number = models.CharField(max_length=15, unique=True)
    number_of_beds = models.IntegerField()
    is_vacant = models.BooleanField(default=True)
    capacity = models.IntegerField()
    description = models.TextField()
    rent_price = models.DecimalField(max_digits=8, decimal_places=2)
    floor = models.CharField(max_length=100)
