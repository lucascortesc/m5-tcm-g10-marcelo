from addresses.models import Address
from django.db.utils import Error
from django.test import TestCase
from employees.models import Employee
from hotels.models import Amenity, Hotel


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

