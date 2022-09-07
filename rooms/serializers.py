from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from rooms.models import Room


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

    def create(self, validated_data):
        room = created = Room.objects.get_or_create(*validated_data)
        if not created:
            raise ValidationError({"Room": "Room already exists."})

        return room