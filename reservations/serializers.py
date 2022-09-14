from datetime import date

from guests.models import Guest
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.serializers import ModelSerializer
from rooms.models import Room

from .models import History, Reservation


class NotFoundError(APIException):
    status_code = 404

class NotAvaliableDate(APIException):
    status_code = 409

class InvalidValue(APIException):
    status_code = 400

class InvalidDate(APIException):
    status_code = 400

class InvalidField(APIException):
    status_code = 400


class ReservationSerializer(ModelSerializer):
    guest_id = serializers.UUIDField()

    class Meta:
        model = Reservation
        fields = "__all__"
        depth = 1

        read_only_fields = ["id", "guest", "room", "total_price"]

    def create(self, data):
        room_id = self.context['room_id']

        if not data['guest']:
            raise NotFoundError({"detail": "Guest not found."})

        guest_id = str(data['guest'][0].id)
        guest = Guest.objects.filter(id=guest_id).first()

        room = Room.objects.filter(id=room_id).first()

        if not room:
            raise NotFoundError({"detail": "Room not found."})

        if not guest:
            raise NotFoundError({"detail": "Guest not found."})

        reservations = Reservation.objects.filter(room_id=room_id)

        checkin = data['checkin']
        checkout = data['checkout']

        if checkin < date.today():
            raise InvalidDate({'detail': 'checkin can not be a past date.'})

        if checkin >= checkout:
            raise InvalidDate({'detail': 'checkout date must be after checkin date.'})

        for reservation in reservations:
            if checkin >= reservation.checkin and checkin < reservation.checkout:
                raise NotAvaliableDate({'detail': 'this date are not avaliable.'})
            if checkout > reservation.checkin and checkout <=reservation.checkout:
                raise NotAvaliableDate({'detail': 'this date are not avaliable.'})
            if checkin < reservation.checkin and checkout > reservation.checkout:
                raise NotAvaliableDate({'detail': 'this date are not avaliable.'})

        if data['total_persons'] > room.capacity:
            raise InvalidValue({'detail': "total persons exceeds the capicity of the room."})

        total_days = (checkout - checkin).days

        data['total_price'] = room.rent_price * total_days

        data['guest'] = guest
        data['room'] = room

        reservation = Reservation.objects.create(**data)

        return reservation


class RetrieveReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
        depth = 1

        read_only_fields = ["id"]

    
    def update(self, instance, data):
        keys = data.keys()
        reservation_id = self.context['reservation_id']
        reservation = Reservation.objects.filter(id=reservation_id).first()
        reservations = Reservation.objects.all()

        if not reservation:
                raise NotFoundError({"detail": "Reservation not found."})

        if "total_price" in keys:
                raise InvalidField({'detail': "you can't change total price, it'll automatically updates."})

        if "guest_id" in keys or "room_id" in keys:
                raise InvalidField({'detail': "to change guest or room you need to do another reservation"})


        if 'checkin' not in keys:
            data['checkin'] = reservation.checkin

        if 'checkout' not in keys:
               data['checkout'] = reservation.checkout

        checkin = data['checkin']
        checkout = data['checkout']

        if checkin < date.today():
             raise InvalidDate({'detail': 'checkin can not be a past date.'})

        if checkin >= checkout:
            raise InvalidDate({'detail': 'checkout date must be after checkin date.'})

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
            if data['total_persons'] > reservation.room.capacity:
                raise InvalidValue({'detail': "total persons exceeds the capicity of the room."})

        total_days = (checkout - checkin).days

        data['total_price'] = reservation.room.rent_price * total_days

        instance = super(RetrieveReservationSerializer, self).update(instance, data)

        return instance

class HistorySerializer(ModelSerializer):
    class Meta:
        model = History
        fields = "__all__"

    