from django.db.models import Avg
from rest_framework import status
from rest_framework.response import Response

from hotel.models import Room, TypeService, UserTypeService, Reservation, CheckIn
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, \
    UpdateAPIView
from rest_framework.permissions import IsAdminUser, BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from hotel.utils import get_intersections
from hotel_api.serializers import RoomSerializer, TypeServiceSerializer, UserTypeServiceSerializer, \
    ReservationSerializer, CreateReservationSerializer, CreateCheckInSerializer, CheckInSerializer


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


class MarkTypeServiceAPI(CreateAPIView):
    queryset = UserTypeService.objects
    serializer_class = UserTypeServiceSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, type_id):
        update_or_create = UserTypeService.objects.update_or_create(
            user_id=request.user.id,
            type_service_id=type_id,
            defaults={"rate": request.data['rate']}
        )
        ts = TypeService.objects.get(id=type_id)
        ts.avg_rate = ts.rated_type_service.aggregate(rate=Avg("rate"))['rate']
        ts.count_rate = ts.users.count()
        ts.save(update_fields=['avg_rate', 'count_rate'])
        serializer = self.serializer_class(update_or_create[0])
        if update_or_create[1]:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateReservationAPI(CreateAPIView):
    queryset = Reservation.objects
    serializer_class = CreateReservationSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        create_serializer = self.serializer_class(data=request.data)
        if create_serializer.is_valid():
            reservation = Reservation(user=request.user, room_id=room_id, **create_serializer.data)
            intersections_of_dates = get_intersections(reservation)
            if intersections_of_dates:
                return Response({'error': 'Дата уже занята'}, status=status.HTTP_400_BAD_REQUEST)
            reservation.save()
            serializer = ReservationSerializer(reservation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(create_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class CreateCheckInAPI(CreateAPIView):
    queryset = Reservation.objects
    serializer_class = CreateCheckInSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request, room_id):
        create_serializer = self.serializer_class(data=request.data)
        if create_serializer.is_valid():
            check_in = CheckIn(user=request.user, room_id=room_id, **create_serializer.data)
            intersections_of_dates = get_intersections(check_in)
            if intersections_of_dates:
                return Response({'error': 'Дата уже занята'}, status=status.HTTP_400_BAD_REQUEST)
            check_in.save()
            serializer = CheckInSerializer(check_in)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(create_serializer.data, status=status.HTTP_400_BAD_REQUEST)