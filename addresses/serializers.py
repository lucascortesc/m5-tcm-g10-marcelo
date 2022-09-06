from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from .models import Address


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

    def create(self, validated_data):
        address, created = Address.objects.get_or_create(**validated_data)
        if not created:
            raise ValidationError({"Address": "Address already in use."})

        return address
