import uuid

from django.db import models


class Employee(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthdate = models.DateField()
    cpf = models.CharField(max_length=11, unique=True)
    function = models.CharField(max_length=200)
    hiring_date = models.DateField()
    salary = models.DecimalField(decimal_places=2, max_digits=10)

    hotel = models.ForeignKey("hotels.Hotel", related_name="employees", on_delete=models.CASCADE)
