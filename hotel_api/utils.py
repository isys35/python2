from django.db.models import Q

from hotel_api import serializers


def validate_intersections(model, data):
    intersections = model.objects.filter(
        Q(started_at__gte=data['started_at'], ended_at__lte=data['ended_at']) |
        Q(started_at__lte=data['started_at'], ended_at__gte=data['ended_at']) |
        Q(started_at__gte=data['started_at'], started_at__lte=data['ended_at'],
          ended_at__gte=data['ended_at']) |
        Q(ended_at__gte=data['started_at'], ended_at__lte=data['ended_at'],
          started_at__lte=data['ended_at'])
    ).filter(room_id=data['room']).exists()
    if intersections:
        raise serializers.ValidationError("Данная дата уже зарезервирована")
    return data