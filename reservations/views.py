from datetime import datetime

from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from employees.permissions import IsAuthenticatedOrAdmin
from guests.models import Guest
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import APIException
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rooms.models import Room

from .models import History, Reservation
from .permissions import RetrieveReservationPermissions
from .serializers import (HistorySerializer, ReservationSerializer,
                          RetrieveReservationSerializer)


class NotFoundError(APIException):
    status_code = 404

class NotAvaliableDate(APIException):
    status_code = 409

class InvalidValue(APIException):
    status_code = 400

class InvalidField(APIException):
    status_code = 400


class ReservationView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrAdmin]

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, room_id):
        room = Room.objects.filter(id=room_id)
        guest = Guest.objects.filter(id=self.request.data['guest_id'])

        if not room:
            raise NotFoundError({"detail": "Room not found."})

        if not guest:
            raise NotFoundError({"detail": "Guest not found."})

        room = room[0]
        guest = guest[0]

        reservations = Reservation.objects.filter(room_id=room_id)

        checkin = datetime.strptime(request.data['checkin'], '%Y-%m-%d').date()
        checkout = datetime.strptime(request.data['checkout'], '%Y-%m-%d').date()

        if checkin >= checkout:
            raise NotAvaliableDate({'detail': 'this date is invalid.'})

        for reservation in reservations:
            if checkin >= reservation.checkin and checkin < reservation.checkout:
                raise NotAvaliableDate({'detail': 'this date are not avaliable.'})
            if checkout > reservation.checkin and checkout <=reservation.checkout:
                raise NotAvaliableDate({'detail': 'this date are not avaliable.'})
            if checkin < reservation.checkin and checkout > reservation.checkout:
                raise NotAvaliableDate({'detail': 'this date are not avaliable.'})

        if request.data['total_persons'] > room.capacity:
            raise InvalidValue({'detail': "total persons exceeds the capicity of the room."})

        total_days = (checkout - checkin).days

        request.data['total_price'] = room.rent_price * total_days

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

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


        def update(self, request, *args, **kwargs):
            partial = kwargs.pop('partial', False)

            keys = request.data.keys()
            reservation_id = self.kwargs['reservation_id']
            reservation = Reservation.objects.filter(id=reservation_id)
            reservations = Reservation.objects.all()

            if not reservation:
                raise NotFoundError({"detail": "Reservation not found."})

            reservation = reservation[0]

            if "total_price" in keys:
                raise InvalidField({'detail': "you can't change total price, it'll automatically updates."})

            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)

            if "guest_id" in keys or "room_id" in keys:
                raise InvalidField({'detail': "to change guest or room you need to do another reservation"})

            if 'checkin' in keys:
                request.data['checkin'] = datetime.strptime(request.data['checkin'], '%Y-%m-%d').date()
            else:
                request.data['checkin'] = reservation.checkin

            if 'checkout' in keys:
                request.data['checkout'] = datetime.strptime(request.data['checkout'], '%Y-%m-%d').date()
            else:
                request.data['checkout'] = reservation.checkout

            checkin = request.data['checkin']
            checkout = request.data['checkout']

            for reservation in reservations:
                if str(reservation.id) == reservation_id:
                    continue
                if checkin >= reservation.checkin and checkin < reservation.checkout:
                    raise NotAvaliableDate({'detail': 'this date are not avaliable.'})
                if checkout > reservation.checkin and checkout <=reservation.checkout:
                    raise NotAvaliableDate({'detail': 'this date are not avaliable.'})
                if checkin < reservation.checkin and checkout > reservation.checkout:
                    raise NotAvaliableDate({'detail': 'this date are not avaliable.'})

            if 'total_persons' in keys:
                if request.data['total_persons'] > reservation.room.capacity:
                    raise InvalidValue({'detail': "total persons exceeds the capicity of the room."})

            total_days = (checkout - checkin).days

            request.data['total_price'] = reservation.room.rent_price * total_days

            serializer.save()

            return Response(serializer.data)


class CheckoutView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrAdmin, RetrieveReservationPermissions]

    queryset = Reservation.objects.all()
    serializer_class = HistorySerializer

    def get(self, request, reservation_id):
        return Response({"detail": "This route is only for checkout, please, use the history route to get all closed reservations"})

    def create(self, request, reservation_id):
        reservation_id = self.kwargs['reservation_id']

        reservation = get_object_or_404(Reservation, id=reservation_id)

        dict_reservation = model_to_dict(reservation)
        dict_reservation['reservation_id'] = reservation_id

        serializer = self.get_serializer(data=dict_reservation)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        reservation.delete()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
