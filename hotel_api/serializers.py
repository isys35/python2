from rest_framework import serializers

from hotel.models import Room, TypeService, UserTypeService


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'number', 'floor', 'number_of_rooms',
                  'description']


class TypeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeService
        fields = ['id', 'title', 'avg_rate', 'count_rate']


class UserTypeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTypeService
        fields = ['user', 'type_service', 'rate']