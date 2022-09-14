from hotels.serializers import AmenitiesSerializer
from rest_framework.exceptions import APIException
from rest_framework.serializers import ModelSerializer

from rooms.models import Room, RoomAmenity


class AlreadyExistsErr(APIException):
    status_code = 409

class RoomSerializer(ModelSerializer):
    amenities = AmenitiesSerializer(many=True)

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
            "amenities",
        ]

        read_only_fields = [
            "id",
            "hotel",
            "is_vacant"
        ]

    def create(self, validated_data):
        amenities_list = validated_data.pop("amenities")

        if Room.objects.filter(number=validated_data['number']):
            raise AlreadyExistsErr({"datail": "Number of the room already exists."})

        room = Room.objects.create(**validated_data)
        
        for amenity in amenities_list:
            amenity_created, _ = RoomAmenity.objects.get_or_create(**amenity)
            amenity_created.room.add(room)
        return room


class RoomAmenitySerializer(ModelSerializer):
    class Meta:
        model = RoomAmenity
        fields = "__all__"
