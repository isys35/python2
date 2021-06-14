from django.db.models import Avg
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from hotel.models import Room, TypeService, UserTypeService, Reservation, CheckIn
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, \
    UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAdminUser, BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from hotel.utils import get_intersections
from hotel_api.serializers import RoomSerializer, TypeServiceSerializer, \
    ReservationSerializer, CreateReservationSerializer, CreateCheckInSerializer, CheckInSerializer, \
    RateTypeServiceSerializer


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class RoomAPIList(ListCreateAPIView):
    queryset = Room.objects
    serializer_class = RoomSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser | ReadOnly]


class RoomAPI(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects
    serializer_class = RoomSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser | ReadOnly]


class TypeServiceAPIList(ListAPIView):
    queryset = TypeService.objects
    serializer_class = TypeServiceSerializer


class PutRateTypeServiceAPI(APIView):
    serializer_class = RateTypeServiceSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        type_service = get_object_or_404(TypeService, id=serializer.data['type_service_id'])
        UserTypeService.objects.update_or_create(
            user_id=request.user.id,
            type_service_id=type_service.id,
            defaults={"rate": serializer.data['rate']}
        )
        type_service.avg_rate = type_service.rated_type_service.aggregate(rate=Avg("rate"))['rate']
        type_service.count_rate = type_service.users.count()
        type_service.save(update_fields=['avg_rate', 'count_rate'])
        return Response({"title": type_service.title,
                         "count_rate": type_service.count_rate,
                         "avg_rate": type_service.avg_rate},
                        status=status.HTTP_201_CREATED)


class CreateReservationAPI(CreateAPIView):
    queryset = Reservation.objects
    serializer_class = CreateReservationSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        room = get_object_or_404(Room, id=serializer.data['room'])
        serializer.is_valid(raise_exception=True)
        self.queryset.create(user=request.user,
                             room_id=room.id,
                             description=serializer.data['description'],
                             started_at=serializer.data['started_at'],
                             ended_at=serializer.data['ended_at'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateCheckInAPI(CreateAPIView):
    queryset = CheckIn.objects
    serializer_class = CreateCheckInSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        room = get_object_or_404(Room, id=serializer.data['room'])
        serializer.is_valid(raise_exception=True)
        self.queryset.create(user=request.user,
                             room_id=room.id,
                             started_at=serializer.data['started_at'],
                             ended_at=serializer.data['ended_at'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)