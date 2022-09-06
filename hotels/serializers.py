from addresses.models import Address
from addresses.serializers import AddressSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from .models import Hotel


class HotelSerializer(ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Hotel
        fields = [
            "id",
            "username",
            "email",
            "password",
            "name",
            "cnpj",
            "address",
            "stars",
        ]
        read_only_fields = [
            "id",
        ]

        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):

        address = validated_data.pop("address")
        serializer = AddressSerializer(data=address)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Hotel.objects.create_user(
            **validated_data, address_id=serializer.data["id"]
        )

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password_to_update = validated_data.pop("password")
            instance.set_password(password_to_update)

        if "address" in validated_data:
            address_to_update = validated_data.pop("address")
            address = Address.objects.get(hotel=instance)

            address_updated = AddressSerializer(
                address, data=address_to_update, partial=True
            )
            address_updated.is_valid(raise_exception=True)
            address_updated.save()

        return super().update(instance, validated_data)
