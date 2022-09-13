import uuid

from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils.timezone import now


class Guest(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthdate = models.DateField()
    email = models.EmailField(unique=True)
    cpf = models.CharField(
        max_length=11,
        validators=[MinLengthValidator(11)]
    )
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
