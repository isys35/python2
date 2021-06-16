from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from hotel.models import Room, Reservation, TypeService, CheckIn


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

    def test_update_room(self):
        # Test for admin-user
        self.client.force_login(self.administrator)
        data = {
            "number": 14,
            "floor": 3,
            "number_of_rooms": 3,
            "description": "test description text",
            "room_class": "ECN"
        }
        book = Room.objects.create(**data)
        url = reverse('hotel-api:room-detail', kwargs={'pk': book.pk})
        data['number_of_rooms'] = 4
        response = self.client.put(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReservationTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser')
        room_data = {
            "number": 14,
            "floor": 3,
            "number_of_rooms": 3,
            "description": "test description text",
            "room_class": "ECN"
        }
        self.room = Room.objects.create(**room_data)
        init_reservation_data = {
            "user_id": self.user.id,
            "room_id": self.room.id,
            "description": "test_description",
            "started_at": datetime(day=1, month=6, year=2021, hour=15, minute=0),
            "ended_at": datetime(day=10, month=6, year=2021, hour=15, minute=0)
        }

        self.init_reservation = Reservation.objects.create(**init_reservation_data)

    def test_create_reservation(self):
        # test create
        self.client.force_login(self.user)
        url = reverse('hotel-api:create-reservation')
        data = {
            "room": self.room.id,
            "description": "test_description",
            "started_at": datetime(day=15, month=6, year=2021, hour=15, minute=0),
            "ended_at": datetime(day=20, month=6, year=2021, hour=15, minute=0)
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # test intersections time
        data['started_at'] = datetime(day=5, month=6, year=2021, hour=15, minute=0),
        data['ended_at'] = datetime(day=15, month=6, year=2021, hour=15, minute=0),
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # test bad room_id
        data = {
            "room": 12,
            "description": "test_description",
            "started_at": datetime(day=20, month=6, year=2021, hour=15, minute=0),
            "ended_at": datetime(day=25, month=6, year=2021, hour=15, minute=0)
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_room_reservations_list(self):
        url = reverse('hotel-api:room-reservations', kwargs={'room_id': self.room.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test bad room_id
        url = reverse('hotel-api:room-reservations', kwargs={'room_id': 31})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PutRateTest(TestCase):

    def setUp(self) -> None:
        self.type_service = TypeService.objects.create(title='Тестовый сервис')
        self.user = User.objects.create_user(username='testuser')

    def test_put_rate(self):
        # test without auth
        data = {
            'rate': 4,
            "type_service_id": self.type_service.id
        }
        url = reverse("hotel-api:put-rate")
        response = self.client.put(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test with auth
        self.client.force_login(self.user)
        response = self.client.put(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CheckInTest(TestCase):

    def setUp(self) -> None:
        self.administrator = User.objects.create_user(username='testadministrator')
        self.administrator.is_staff = True
        self.administrator.save()
        self.user = User.objects.create_user(username='testuser')
        room_data = {
            "number": 14,
            "floor": 3,
            "number_of_rooms": 3,
            "description": "test description text",
            "room_class": "ECN"
        }
        self.room = Room.objects.create(**room_data)
        init_checkin_data = {
            "user_id": self.user.id,
            "room_id": self.room.id,
            "started_at": datetime(day=1, month=6, year=2021, hour=15, minute=0),
            "ended_at": datetime(day=10, month=6, year=2021, hour=15, minute=0)
        }
        self.init_checkin = CheckIn.objects.create(**init_checkin_data)

    def test_create_checkin(self):
        # test create by user
        self.client.force_login(self.user)
        url = reverse('hotel-api:create-checkin')
        data = {
            "user": self.user.id,
            "room": self.room.id,
            "started_at": datetime(day=15, month=6, year=2021, hour=15, minute=0),
            "ended_at": datetime(day=20, month=6, year=2021, hour=15, minute=0)
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # test create by administrator
        self.client.force_login(self.administrator)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class MessageTest(TestCase):

    def setUp(self) -> None:
        self.administrator = User.objects.create_user(username='testadministrator')
        self.administrator.is_staff = True
        self.administrator.save()
        self.user = User.objects.create_user(username='testuser')

    def test_send_message(self):
        self.client.force_login(self.user)
        url = reverse('hotel-api:send-message')
        data = {
            "text": "test text",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # test message-history
        self.client.force_login(self.administrator)
        url_message_history = reverse('hotel-api:message-history', kwargs={'user_id': self.user.id})
        response = self.client.get(url_message_history)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AvgRateAllServicesTest(TestCase):
    def setUp(self) -> None:
        self.type_service_1 = TypeService.objects.create(title='Тестовый сервис 1', avg_rate=3)
        self.type_service_2 = TypeService.objects.create(title='Тестовый сервис 2', avg_rate=4)
        self.type_service_3 = TypeService.objects.create(title='Тестовый сервис 3', avg_rate=5)

    def test_avg_all_ts_rates(self):
        url = reverse('hotel-api:avg-rate-all-services')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['avg_rate'], '4.00')