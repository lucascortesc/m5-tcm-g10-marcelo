import operator
from functools import reduce

from django.db.models import Q
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rooms.models import Room, RoomAmenity
from rooms.serializers import RoomSerializer


class RoomView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def perform_create(self, serializer):
        serializer.save(hotel=self.request.user)

    def get_queryset(self):
        params_amenities = self.request.GET.getlist('amenities')
        # rooms = Room.objects.all()

        # filtred_rooms = []

        # for room in rooms:
        #     length = len(params_amenities)

        #     for amenity in room.amenities.all():
        #         if amenity.name in params_amenities:
        #             length -= 1 

        #     if length == 0:
        #         filtred_rooms.append(room)
                    
        # return filtred_rooms

        queryset = Room.objects.all()
        for search_term in params_amenities:
            queryset = queryset.filter(amenities__name=search_term) 
        
        return queryset

        

class RoomDetailView(generics.RetrieveUpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    lookup_url_kwarg = "room_id"
