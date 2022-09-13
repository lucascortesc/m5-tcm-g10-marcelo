from addresses.models import Address
from django.test import TestCase
from guests.models import Guest
from hotels.models import Hotel
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from rooms.models import Room

from .models import Reservation


# Create your tests here.
class ReservationTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.guest = Guest.objects.create(
            first_name="José",
            last_name="Ricardo",
            birthdate="2002-05-05",
            email="josericardo@mail.com",
            cpf="12345678910",
        )
        cls.address = Address.objects.create(
            street="Angel Avenue",
            number=129,
            city="Orlando",
            state="Florida",
            zip_code="32808000",
        )

        cls.hotelTest = Hotel.objects.create(
            name="Hotel teaste2",
            cnpj="12345202241",
            username="tes2222322",
            password="salve",
            email="teste@mail.com",
            address=cls.address,
            stars=1,
        )
        cls.room = Room.objects.create(
            number=104,
            number_of_beds=5,
            is_vacant=False,
            capacity=7,
            description="Teste",
            rent_price=120.00,
            floor="2",
            hotel=cls.hotelTest,
        )

        cls.checkin = "2022-10-10"
        cls.checkout = "2022-10-30"
        cls.total_persons = 3
        cls.total_price = 25.00

    def test_create(self):
        reservation = Reservation.objects.create(
            checkin=self.checkin,
            checkout=self.checkout,
            total_persons=self.total_persons,
            total_price=self.total_price,
            guest=self.guest,
            room=self.room,
        )
        self.assertIsNotNone(reservation.id)

    def test_create_wrong_fields(self):
        with self.assertRaises(TypeError):
            reservation = Reservation.objects.create(
                checkin=1234,
                checkout=self.checkout,
                total_persons=self.total_persons,
                total_price=self.total_price,
                guest=self.guest,
                room=self.room,
            )


class ReservationViewsTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.address = Address.objects.create(
            street="Angel Avenue",
            number=129,
            city="Orlan2do22222a22aa22aaaaa",
            state="Florida",
            zip_code="32808000",
        )
        cls.guest = Guest.objects.create(
            first_name="José",
            last_name="Ricardo",
            birthdate="2002-05-05",
            email="josericardo@mail.com",
            cpf="12345678910",
        )
        cls.hotelTest = Hotel.objects.create(
            name="Hotel teaste2",
            cnpj="12345202241",
            username="tes2222322",
            password="salve",
            email="teste@mail.com",
            address=cls.address,
            stars=1,
        )
        cls.room = Room.objects.create(
            number=104,
            number_of_beds=5,
            is_vacant=False,
            capacity=7,
            description="Teste",
            rent_price=120.00,
            floor="2",
            hotel=cls.hotelTest,
        )
        cls.total = 123
        cls.user_token = Token.objects.create(user=cls.hotelTest)

    def test_list_reservation(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.get("/api/rooms/" + str(self.room.id) + "/reservations/")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
