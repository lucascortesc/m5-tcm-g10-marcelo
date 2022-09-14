# Generated by Django 4.1.1 on 2022-09-13 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("number", models.CharField(max_length=15, unique=True)),
                ("number_of_beds", models.IntegerField()),
                ("is_vacant", models.BooleanField(default=True)),
                ("capacity", models.IntegerField()),
                ("description", models.TextField()),
                ("rent_price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("floor", models.CharField(max_length=100)),
                (
                    "hotel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rooms",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RoomAmenity",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "room",
                    models.ManyToManyField(related_name="amenities", to="rooms.room"),
                ),
            ],
        ),
    ]
