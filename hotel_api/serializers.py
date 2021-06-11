from rest_framework import serializers
from rest_framework.fields import CharField

from hotel.models import Room, TypeService, UserTypeService, Reservation, CheckIn


class TypeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeService
        fields = ['id', 'title', 'avg_rate', 'count_rate']


class UserTypeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTypeService
        fields = ['rate']


class ReservationSerializer(serializers.ModelSerializer):
    user = CharField(source="user.username")

    class Meta:
        model = Reservation
        fields = ['user', 'description', 'started_at', 'ended_at']


class CreateReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['description', 'started_at', 'ended_at']


class CheckInSerializer(serializers.ModelSerializer):
    user = CharField(source="user.username")

    class Meta:
        model = CheckIn
        fields = ['user', 'started_at', 'ended_at']


class RoomSerializer(serializers.ModelSerializer):
    booked = ReservationSerializer(many=True, read_only=True)
    check_ins = CheckInSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'number', 'floor', 'number_of_rooms',
                  'description', 'booked', 'check_ins']
