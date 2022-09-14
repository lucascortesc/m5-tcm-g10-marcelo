from dataclasses import field

from addresses.models import Address
from addresses.serializers import AddressSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from .models import Amenity, Hotel


class AmenitiesSerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "name"]


class HotelSerializer(ModelSerializer):
    address = AddressSerializer()
    amenities = AmenitiesSerializer(many=True)

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
            "amenities",
        ]
        read_only_fields = [
            "id",
        ]

        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        if len(validated_data["cnpj"]) < 14:
            raise ValidationError({"detail": "Your CNPJ must contain 14 Digits."})

        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        for digit in validated_data["cnpj"]:
            if digit not in numbers:
                raise ValidationError({"detail": "Your CNPJ must contain only Digits."})

        address = validated_data.pop("address")
        serializer_address = AddressSerializer(data=address)
        serializer_address.is_valid(raise_exception=True)
        serializer_address.save()

        amenities_list = validated_data.pop("amenities")

        hotel = Hotel.objects.create_user(
            **validated_data, address_id=serializer_address.data["id"]
        )

        for amenity in amenities_list:
            amenity_created, _ = Amenity.objects.get_or_create(**amenity)
            amenity_created.hotel.add(hotel)

        return hotel

    def update(self, instance, validated_data):

        if "cnpj" in validated_data:
            if len(validated_data["cnpj"]) < 14:
                raise ValidationError({"detail": "Your CNPJ must contain 14 Digits."})

            numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

            for digit in validated_data["cnpj"]:
                if digit not in numbers:
                    raise ValidationError(
                        {"detail": "Your CNPJ must contain only Digits."}
                    )

        if "amenities" in validated_data:
            raise ValidationError(
                "Amenities: Use UPDATE /api/hotels/amenities/amenity_id/ to update an amenity."
            )
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
