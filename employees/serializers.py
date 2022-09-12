from hotels.models import Hotel
from rest_framework import serializers

from employees.models import Employee


class EmployeeHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ["id", "name", "email", "cnpj"]
        read_only_fields = ["id", "name", "email", "cnpj"]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "first_name", "last_name", "birthdate", "cpf", "function", "hiring_date", "salary", "hotel_id"]
        read_only_fields = ["id"]


class EmployeeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "first_name", "last_name", "birthdate", "cpf", "function", "hiring_date", "salary", "hotel"]
        read_only_fields = ["id"]

    hotel = EmployeeHotelSerializer(read_only=True)
