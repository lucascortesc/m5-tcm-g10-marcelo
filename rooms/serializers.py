from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from rooms.models import Room, RoomAmenity


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

    def create(self, validated_data):
        room, created = Room.objects.get_or_create(*validated_data)
        if not created:
            raise ValidationError({"Room": "Room already exists."})

        return room


class RoomAmenitySerializer(ModelSerializer):
    class Meta:
        model = RoomAmenity
        fields = "__all__"

    def create(self, validated_data):
        amenity, created = RoomAmenity.objects.get_or_create(*validated_data)
        if not created:
            raise ValidationError({"Amenity": "Amenity already exists."})

        return amenity
