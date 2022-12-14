from django_filters.rest_framework import DjangoFilterBackend
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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "number_of_beds",
        "capacity",
        "rent_price",
       
    ]
    def perform_create(self, serializer):
       
        serializer.save(hotel=self.request.user)

    def get_queryset(self):

        params_amenities = self.request.GET.getlist('amenities')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        queryset = Room.objects.all()
        for search_term in params_amenities:
            queryset = queryset.filter(amenities__name=search_term)

        if min_price:
            queryset = queryset.filter(rent_price__gte=min_price)

        if max_price:
            queryset = queryset.filter(rent_price__lte=max_price)  
        
        return queryset


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    lookup_url_kwarg = "room_id"
