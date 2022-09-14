from addresses.models import Address
from django.db.utils import Error
from django.test import TestCase
from django.urls import reverse
from hotels.models import Amenity, Hotel
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status

from employees.models import Employee


class EmployeeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.employee_data = {
            "first_name": "Alfred",
            "last_name": "Pennyworth",
            "birthdate": "1950-01-01",
            "cpf": "11111111111",
            "function": "zelador",
            "hiring_date": "1997-01-01",
            "salary": 1999.00
        }

        hotel_data = {
            "username": "kenzie",
            "name": "Kenzie Hotel",
            "email": "kenzie@mail.com",
            "password": "1234",
            "cnpj": "123456789",
            "stars": 5,
        }

        address = {
                "street": "rua",
                "number": 10,
                "city": "city",
                "state": "state",
                "zip_code": "12345678",
                "complement": "house"
        }

        amenities_list = [
                {"name": "Ocean View"}
        ]

        cls.address, _ = Address.objects.get_or_create(**address)
        cls.hotel = Hotel.objects.create_user(**hotel_data, address_id=cls.address.id)

        for amenity in amenities_list:
            amenity_created, _ = Amenity.objects.get_or_create(**amenity)
            amenity_created.hotel.add(cls.hotel)

        cls.employee = Employee.objects.create(**cls.employee_data, hotel_id=cls.hotel.id)

    def test_cannot_register_employee_with_duplicated_cpf(self):
        with self.assertRaises(Error):
            Employee.objects.create(**self.employee_data)

    def test_cpf_max_length(self):
        max_length = self.employee._meta.get_field("cpf").max_length

        self.assertEqual(max_length, 11)



class EmployeeViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.employee_data_1 = {
            "first_name": "Alfred",
            "last_name": "Pennyworth",
            "birthdate": "1950-01-01",
            "cpf": "00000000000",
            "function": "zelador",
            "hiring_date": "1997-01-01",
            "salary": 1999.00
        }

        hotel_data = {
            "username": "kenzie",
            "name": "Kenzie Hotel",
            "email": "kenzie@mail.com",
            "password": "1234",
            "cnpj": "123456789",
            "stars": 5,
        }

        amenities_list = [
                {"name": "Ocean View"}
        ]

        address_1 = {
                "street": "rua",
                "number": 10,
                "city": "city",
                "state": "state",
                "zip_code": "12345678",
                "complement": "house"
        }

        cls.address, _ = Address.objects.get_or_create(**address_1)
        cls.hotel_1 = Hotel.objects.create_user(**hotel_data, address_id=cls.address.id)
        cls.hotel_1_token = Token.objects.create(user=cls.hotel_1)

        for amenity in amenities_list:
            amenity_created, _ = Amenity.objects.get_or_create(**amenity)
            amenity_created.hotel.add(cls.hotel_1)

        cls.list_create_url = reverse("list-create-employee")

    def test_unauthenticated_hotel_user_can_add_employee(self):
        response = self.client.post(self.list_create_url, data=self.employee_data_1)

        expected_status_code = status.HTTP_401_UNAUTHORIZED

        self.assertEqual(expected_status_code, response.status_code)

    def test_authenticated_hotel_user_can_add_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.hotel_1_token.key)

        response = self.client.post(self.list_create_url, data=self.employee_data_1)

        expected_status_code = status.HTTP_201_CREATED

        self.assertEqual(expected_status_code, response.status_code)

    def test_unauthenticated_user_can_list_employees(self):
        response = self.client.get(self.list_create_url)

        expected_status_code = status.HTTP_401_UNAUTHORIZED

        self.assertEqual(expected_status_code, response.status_code)

    def test_authenticated_hotel_user_can_list_employees(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.hotel_1_token.key)

        response = self.client.get(self.list_create_url)

        expected_status_code = status.HTTP_200_OK

        self.assertEqual(expected_status_code, response.status_code)


class EmployeeDetailViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.employee_data_1 = {
            "first_name": "Alfred",
            "last_name": "Pennyworth",
            "birthdate": "1950-01-01",
            "cpf": "00000000000",
            "function": "zelador",
            "hiring_date": "1997-01-01",
            "salary": 1999.00
        }

        hotel_data = {
            "username": "kenzie",
            "name": "Kenzie Hotel",
            "email": "kenzie@mail.com",
            "password": "1234",
            "cnpj": "123456789",
            "stars": 5,
        }

        address_1 = {
                "street": "rua",
                "number": 10,
                "city": "city",
                "state": "state",
                "zip_code": "12345678",
                "complement": "house"
        }

        amenities_list = [
                {"name": "Ocean View"}
        ]

        cls.address, _ = Address.objects.get_or_create(**address_1)
        cls.hotel_1 = Hotel.objects.create_user(**hotel_data, address_id=cls.address.id)
        cls.hotel_1_token = Token.objects.create(user=cls.hotel_1)

        for amenity in amenities_list:
            amenity_created, _ = Amenity.objects.get_or_create(**amenity)
            amenity_created.hotel.add(cls.hotel_1)

        cls.employee_1 = Employee.objects.create(**cls.employee_data_1, hotel_id=cls.hotel_1.id)

        cls.retrieve_update_delete_url = reverse("list-create-detail-employee", kwargs={"employee_id": cls.employee_1.id})

    def test_unauthenticated_retrieve_employee(self):
        response = self.client.get(self.retrieve_update_delete_url)

        expected_status_code = status.HTTP_401_UNAUTHORIZED

        self.assertEqual(expected_status_code, response.status_code)

    def test_unauthenticated_update_employee(self):
        response = self.client.patch(self.retrieve_update_delete_url, data={"name": "PATCH"})

        expected_status_code = status.HTTP_401_UNAUTHORIZED

        self.assertEqual(expected_status_code, response.status_code)

    def test_unauthenticated_delete_employee(self):
        response = self.client.delete(self.retrieve_update_delete_url)

        expected_status_code = status.HTTP_401_UNAUTHORIZED

        self.assertEqual(expected_status_code, response.status_code)

    def test_authenticated_retrieve_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.hotel_1_token.key)

        response = self.client.get(self.retrieve_update_delete_url)

        expected_status_code = status.HTTP_200_OK

        self.assertEqual(expected_status_code, response.status_code)

    def test_authenticated_update_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.hotel_1_token.key)

        response = self.client.patch(self.retrieve_update_delete_url, data={"name": "PATCH"})

        expected_status_code = status.HTTP_200_OK

        self.assertEqual(expected_status_code, response.status_code)

    def test_authenticated_delete_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.hotel_1_token.key)

        response = self.client.delete(self.retrieve_update_delete_url)

        expected_status_code = status.HTTP_204_NO_CONTENT

        self.assertEqual(expected_status_code, response.status_code)
        