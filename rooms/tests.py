from rest_framework.authtoken.models import Token
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import Response, status
from addresses.serializers import AddressSerializer
from hotels.models import Hotel
from rooms.models import Room, RoomAmenity


class RoomsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.hotel_1_data = {
            "username": "Hostil2",
            "name": "hostil2",
            "cnpj": "00000000000002",
            "stars": 5,
            "password": "abdc1234#",
            "address": {
                "street": "rua2",
                "number": 2,
                "city": "cidade",
                "state": "estado",
                "zip_code": "00000000",
            },
            "amenities": [{"name": "cama dura"}]
        }
   
        cls.room_1_data = {
            "number": "7",
            "number_of_beds": 2,
            "is_vacant": True,
            "capacity": 3,
            "description": "pequeno",
            "rent_price": "50.00",
            "floor": "2",
            "amenities": [{"name": "ar condicionado"}]
        }

        cls.validated_data = cls.hotel_1_data
        cls.address = cls.validated_data.pop("address")
        serializer_address = AddressSerializer(data=cls.address)
        serializer_address.is_valid(raise_exception=True)
        serializer_address.save()

        cls.amenities_list = cls.validated_data.pop("amenities")

        cls.hotel = Hotel.objects.create_user(
            **cls.validated_data, address_id=serializer_address.data["id"]
        )
        cls.validated_data = cls.room_1_data
        amenities_list = cls.validated_data.pop("amenities")

        cls.room = Room.objects.create(**cls.validated_data, hotel=cls.hotel)
        for amenity in amenities_list:
            amenity_created, _ = RoomAmenity.objects.get_or_create(**amenity)
            amenity_created.room.add(cls.room)

    
    
    def test_hotel_can_create_room(self):
        self.assertTrue(self.room)

    
    
    def test_product_fields(self):

        self.assertEqual(self.room.number, self.room_1_data["number"])
        self.assertEqual(self.room.number_of_beds, self.room_1_data["number_of_beds"])
        self.assertEqual(self.room.description, self.room_1_data["description"])
        self.assertEqual(self.room.rent_price, self.room_1_data["rent_price"])


class RoomsListViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client: APIClient
        cls.base_url = "/api/rooms/"
        cls.hotel_1_data = {
            "username": "Hostil4",
            "name": "hostil4",
            "cnpj": "00000000000004",
            "stars": 5,
            "password": "abdc1234#",
            "address": {
                "street": "rua4",
                "number": 4,
                "city": "cidade",
                "state": "estado",
                "zip_code": "00000000",
            },
            "amenities": [{"name": "cama dura"}]
        }
   
        cls.room_1_data = {
            "number": "9",
            "number_of_beds": 2,
            "is_vacant": True,
            "capacity": 3,
            "description": "pequeno",
            "rent_price": "50.00",
            "floor": "2",
            "amenities": [{"name": "ar condicionado"}]
        }

        cls.validated_data = cls.hotel_1_data
        cls.address = cls.validated_data.pop("address")
        serializer_address = AddressSerializer(data=cls.address)
        serializer_address.is_valid(raise_exception=True)
        serializer_address.save()

        cls.amenities_list = cls.validated_data.pop("amenities")

        cls.hotel = Hotel.objects.create_user(
            **cls.validated_data, address_id=serializer_address.data["id"]
        )
        cls.hotel_token = Token.objects.create(user=cls.hotel)


    def test_can_create_room(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.hotel_token.key)
        response = self.client.post(self.base_url, data=self.room_1_data)
 
        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)


    def test_can_list_room(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.hotel_token.key)
        response = self.client.get(self.base_url, data=self.room_1_data)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
    