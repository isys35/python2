from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from rest_framework.fields import CharField
from .utils import validate_intersections

from hotel.models import Room, TypeService, Reservation, CheckIn, Message


class TypeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeService
        fields = ['id', 'title', 'avg_rate', 'count_rate']


class RateTypeServiceSerializer(serializers.Serializer):
    rate = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    type_service_id = serializers.IntegerField()


class ReservationSerializer(serializers.ModelSerializer):
    user = CharField(source="user.username")

    class Meta:
        model = Reservation
        fields = ['user', 'room', 'description', 'started_at', 'ended_at']


class CreateReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["room", 'description', 'started_at', 'ended_at']

    def validate(self, data):
        return validate_intersections(Reservation, data)


class CheckInSerializer(serializers.ModelSerializer):
    user = CharField(source="user.username")

    class Meta:
        model = CheckIn
        fields = ['user', 'room', 'started_at', 'ended_at']


class CreateCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = ['user', 'room', 'started_at', 'ended_at']

    def validate(self, data):
        return validate_intersections(CheckIn, data)


class RoomSerializer(serializers.ModelSerializer):
    booked = ReservationSerializer(many=True, read_only=True)
    check_ins = CheckInSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'number', 'floor', 'number_of_rooms',
                  'description', 'room_class', 'booked', 'check_ins']


class CreateMessageSerializer(serializers.Serializer):
    text = serializers.CharField()


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['text', 'pub_date']