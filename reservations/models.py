import uuid

from django.db import models


class Reservation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    checkin = models.DateField()
    checkout = models.DateField()
    total_persons = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    guest = models.ForeignKey(
        "guests.Guest", on_delete=models.CASCADE, related_name="reservations"
    )

    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, related_name="reservations"
    )


class History(Reservation):
    reservation_id = models.CharField(max_length=255)
