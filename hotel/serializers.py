from rest_framework import serializers

from hotel.models import TypeService


class TypeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeService
        fields = ['title', 'avg_rate', 'count_rate']

