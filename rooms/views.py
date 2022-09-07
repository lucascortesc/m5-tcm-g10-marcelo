from rest_framework import generics

from rooms.models import Room
from rooms.serializers import RoomSerializer


class RoomView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomDetailView(generics.RetrieveUpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    lookup_url_kwarg = "room_id"
    