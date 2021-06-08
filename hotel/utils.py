from django.db.models import Q


def get_intersections(instance):
    intersections = instance.__class__.objects.filter(
        Q(started_at__gte=instance.started_at, ended_at__lte=instance.ended_at) |
        Q(started_at__lte=instance.started_at, ended_at__gte=instance.ended_at) |
        Q(started_at__gte=instance.started_at, started_at__lte=instance.ended_at,
          ended_at__gte=instance.ended_at) |
        Q(ended_at__gte=instance.started_at, ended_at__lte=instance.ended_at,
          started_at__lte=instance.ended_at)
    ).filter(room_id=instance.room_id)
    return intersections
