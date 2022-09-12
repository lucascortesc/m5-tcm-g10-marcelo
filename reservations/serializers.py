from rest_framework.serializers import ModelSerializer

from .models import Reservation


class ReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
        depth = 1

        read_only_fields = ["id", "guest", "room"]


class RetrieveReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
        depth = 1

        read_only_fields = ["id"]
