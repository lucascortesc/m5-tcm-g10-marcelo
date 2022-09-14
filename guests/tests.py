from addresses.models import Address
from django.db.utils import Error
from django.test import TestCase
from hotels.models import Hotel
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status

from .models import Guest


class GuestTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.first_name = "José"
        cls.last_name = "Ricardo"
        cls.birthdate = "2002-05-05"
        cls.email = "josericardo@mail.com"
        cls.cpf = "12345678910"

        Guest.objects.create(
            first_name=cls.first_name,
            last_name=cls.last_name,
            birthdate=cls.birthdate,
            cpf=cls.cpf,
            email=cls.email,
        )

    def test_error_same_cpf(self):
        with self.assertRaises(Error):
            Guest.objects.create(
                first_name="Vasco",
                last_name="Da Gama",
                birthdate="2002-04-02",
                cpf=self.cpf,
                email="vascodagama@mail.com",
            )

    def test_create_guest(self):
        guest = Guest.objects.create(
            first_name="Vasco",
            last_name="Da Gama",
            birthdate="2002-04-02",
            cpf="12345678920",
            email="vascodagama@mail.com",
        )
        self.assertIsNotNone(guest.id)


class GuestViewsTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.address = Address.objects.create(
            street="Angel Avenue",
            number=129,
            city="Orlan2do22222a22aa22aaaaa",
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
        cls.user_token = Token.objects.create(user=cls.hotelTest)

    def test_create_guest(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.post(
            "/api/guests/",
            data={
                "first_name": "Vasco",
                "last_name": "Da Gama",
                "birthdate": "2002-04-02",
                "cpf": "12345678922",
                "email": "vascodagama@mail.com",
            },
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_unhautorized_create_guest(self):
        response = self.client.post(
            "/api/guests/",
            data={
                "first_name": "Vasco",
                "last_name": "Da Gama",
                "birthdate": "2002-04-02",
                "cpf": "12345678922",
                "email": "vascodagama@mail.com",
            },
        )
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_list_guests(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.get("/api/guests/")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_create_wrong_guest(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token.key)
        response = self.client.post(
            "/api/guests/",
            data={"first_name": "missing keys"},
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
