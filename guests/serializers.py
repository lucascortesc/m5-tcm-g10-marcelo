from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from .models import Guest


class GuestSerializer(ModelSerializer):
    class Meta:
        model = Guest
        fields = [
            "id",
            "first_name",
            "last_name",
            "birthdate",
            "email",
            "cpf",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        for digit in validated_data["cpf"]:
            if digit not in numbers:
                raise ValidationError({"detail": "Your CNPJ must contain only Digits."})

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "cpf" in validated_data:
            numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

            for digit in validated_data["cpf"]:
                if digit not in numbers:
                    raise ValidationError(
                        {"detail": "Your CPF must contain only Digits."}
                    )

        return super().update(instance, validated_data)
