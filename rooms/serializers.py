from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from hotels.serializers import AmenitiesSerializer
from rooms.models import Room, Amenity


class RoomSerializer(ModelSerializer):
    #amenities = AmenitiesSerializer(many=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "number",
            "number_of_beds",
            "is_vacant",
            "capacity",
            "description",
            "rent_price",
            "floor",
            "hotel",
        ]

        read_only_fields = [
            "id",
            "hotel",
        ]


class RoomAmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"
