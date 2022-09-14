# Generated by Django 4.1.1 on 2022-09-13 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("guests", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="guest",
            name="hotel",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="guests",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
