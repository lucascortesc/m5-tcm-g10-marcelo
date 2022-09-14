from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from employees.permissions import IsAuthenticatedOrAdmin
from guests.models import Guest
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView
from rooms.models import Room

from .models import History, Reservation
from .permissions import ReservationPermissions, RetrieveReservationPermissions
from .serializers import (HistorySerializer, ReservationSerializer,
                          RetrieveReservationSerializer)
from django_filters.rest_framework import DjangoFilterBackend

class AllReservationView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrAdmin]

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

<<<<<<< HEAD
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "guest",
        "room",
        
    ]

=======
    def get_queryset(self):
        hotel_id = self.request.user.id
        query_set = [reservation for reservation in self.queryset.all() if reservation.room.hotel.id == hotel_id]

        return query_set
>>>>>>> bba135d937d26fad147386440b92ccbc31229cbd

class AllHistoryView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrAdmin]

    queryset = History.objects.all()
    serializer_class = HistorySerializer

    def get_queryset(self):
        hotel_id = self.request.user.id
        query_set = [history for history in self.queryset.all() if history.room.hotel.id == hotel_id]
          
        return query_set

class ReservationView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrAdmin, ReservationPermissions]

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['room_id'] = self.kwargs['room_id']

        return context

    def create(self, request, room_id):

        serializer = self.get_serializer(data=request.data)

        room = Room.objects.filter(id=room_id)

        if not room:
            return Response({"detail": "Room not found."}, status=status.HTTP_404_NOT_FOUND)

        room = room[0]

        room.is_vacant = False
        room.save()

        self.check_object_permissions(request=request, obj=room)

        serializer.is_valid(raise_exception=True)

        guest = Guest.objects.filter(id=self.request.data['guest_id'])

        serializer.save(room=room, guest=guest)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
   

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return self.queryset.filter(room_id=room_id)

class RetrieveReservationView(RetrieveUpdateDestroyAPIView):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticatedOrAdmin, RetrieveReservationPermissions]

        queryset = Reservation.objects.all()
        serializer_class = RetrieveReservationSerializer 
        lookup_url_kwarg = "reservation_id"

        def get_serializer_context(self):
            context = super().get_serializer_context()
            context['reservation_id'] = self.kwargs['reservation_id']

            return context


        def update(self, request, *args, **kwargs):
            partial = kwargs.pop('partial', False)

            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(serializer.data)


class CheckoutView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrAdmin, RetrieveReservationPermissions]

    queryset = Reservation.objects.all()
    serializer_class = HistorySerializer

    def create(self, request, reservation_id):
        reservation_id = self.kwargs['reservation_id']

        reservation = get_object_or_404(Reservation, id=reservation_id)

        dict_reservation = model_to_dict(reservation)
        dict_reservation['reservation_id'] = reservation_id

        serializer = self.get_serializer(data=dict_reservation)
        serializer.is_valid(raise_exception=True)

        # room.is_vacant = True
        # room.save()

        serializer.save()

        reservation.delete()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
