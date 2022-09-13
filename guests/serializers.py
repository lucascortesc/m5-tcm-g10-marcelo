from rest_framework.serializers import ModelSerializer

from .models import Guest


class GuestSerializer(ModelSerializer):
    class Meta:
        model = Guest
        fields = ["id", "first_name", "last_name", "birthdate", "email", "cpf", "created_at", "updated_at"]

        read_only_fields = ["id", "created_at", "updated_at"]
