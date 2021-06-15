from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from hotel.models import Room


class CRUDRoomTest(TestCase):

    def setUp(self) -> None:
        self.administrator = User.objects.create_user(username='testadministrator')
        self.administrator.is_staff = True
        self.administrator.save()
        self.user = User.objects.create_user(username='testuser')

    def test_create_room(self):
        # Test for admin-user
        self.client.force_login(self.administrator)
        url = reverse('hotel-api:rooms')
        data = {
            "number": 14,
            "floor": 3,
            "number_of_rooms": 3,
            "description": "test description text",
            "room_class": "ECN"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['number'], data['number'])
        self.assertEqual(response.data['floor'], data['floor'])
        self.assertEqual(response.data['number_of_rooms'], data['number_of_rooms'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['room_class'], data['room_class'])
        room = Room.objects.get(**data)
        self.assertEqual(response.data['id'], room.id)
        # Test for user
        self.client.force_login(self.user)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)