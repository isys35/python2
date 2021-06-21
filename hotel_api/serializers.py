from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from rest_framework.fields import CharField
from .utils import validate_intersections

from hotel.models import Room, TypeService, Reservation, CheckIn, Message


class TypeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeService
        fields = ['id', 'title', 'avg_rate', 'count_rate']


class AvgAllServices(serializers.Serializer):
    avg_rate = serializers.DecimalField(max_digits=4,
                                        decimal_places=2,
                                        validators=[MinValueValidator(0), MaxValueValidator(5)])


class RateTypeServiceSerializer(serializers.Serializer):
    rate = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    type_service_id = serializers.IntegerField()


class ReservationSerializer(serializers.ModelSerializer):
    user = CharField(source="user.username")
    started_at = serializers.SerializerMethodField()
    ended_at = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ['user', 'room', 'description', 'started_at', 'ended_at']

    def get_started_at(self, instance):
        return instance.started_at.strftime("%d.%m.%Y %H:%M")

    def get_ended_at(self, instance):
        return instance.ended_at.strftime("%d.%m.%Y %H:%M")


class CreateReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["room", 'description', 'started_at', 'ended_at']

    def validate(self, data):
        return validate_intersections(Reservation, data)


class CreateCheckInSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = CheckIn
        fields = ['username', 'room', 'started_at', 'ended_at']

    def validate(self, data):
        return validate_intersections(CheckIn, data)


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'number', 'floor', 'number_of_rooms',
                  'description', 'room_class']


class CreateMessageSerializer(serializers.Serializer):
    text = serializers.CharField()


class MessageSerializer(serializers.ModelSerializer):
    pub_date = serializers.SerializerMethodField()
    username = serializers.CharField(source='author.username')

    class Meta:
        model = Message
        fields = ['text', 'pub_date', 'username']

    def get_pub_date(self, instance):
        return instance.pub_date.strftime("%d.%m.%Y %H:%M")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CheckInSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    room = CharField(source="room.number")
    started_at = serializers.SerializerMethodField()
    ended_at = serializers.SerializerMethodField()
    last_message_today = MessageSerializer(read_only=True)

    class Meta:
        model = CheckIn
        fields = ['user', 'room', 'started_at', 'ended_at', 'last_message_today']

    def get_started_at(self, instance):
        return instance.started_at.strftime("%d.%m.%Y %H:%M")

    def get_ended_at(self, instance):
        return instance.ended_at.strftime("%d.%m.%Y %H:%M")


class RoomSerializer(serializers.ModelSerializer):
    booked = ReservationSerializer(many=True, read_only=True)
    check_ins = CheckInSerializer(many=True, read_only=True)
    room_class = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'number', 'floor', 'number_of_rooms',
                  'description', 'room_class', 'booked', 'check_ins']

    def get_room_class(self, instance):
        return instance.get_room_class_display()


class UserLoginSerializer(serializers.ModelSerializer):
    username = CharField()
    password = CharField()

    class Meta:
        model = User
        fields = ['username', 'password']
