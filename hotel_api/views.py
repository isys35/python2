import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.db.models import Avg, Subquery, OuterRef
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from hotel.models import Room, TypeService, UserTypeService, Reservation, CheckIn, Message
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAdminUser, BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from hotel_api.serializers import RoomSerializer, TypeServiceSerializer, \
    CreateReservationSerializer, CreateCheckInSerializer, \
    RateTypeServiceSerializer, ReservationSerializer, CheckInSerializer, CreateMessageSerializer, MessageSerializer, \
    AvgAllServices, CreateRoomSerializer


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class RoomAPIList(ListAPIView):
    queryset = Room.objects
    serializer_class = RoomSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class CreateRoomAPI(ListCreateAPIView):
    queryset = Room.objects
    serializer_class = CreateRoomSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]


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
        ts_serializer = TypeServiceSerializer(type_service)
        return Response(ts_serializer.data,
                        status=status.HTTP_201_CREATED)


class CreateReservationAPI(CreateAPIView):
    queryset = Reservation.objects
    serializer_class = CreateReservationSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        room = get_object_or_404(Room, id=serializer.data['room'])
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
        serializer.is_valid(raise_exception=True)
        room = get_object_or_404(Room, id=serializer.data['room'])
        user = get_object_or_404(User, username=serializer.data['username'])
        self.queryset.create(user=user,
                             room_id=room.id,
                             started_at=serializer.data['started_at'],
                             ended_at=serializer.data['ended_at'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReservationAPIList(ListAPIView):
    queryset = Reservation.objects
    serializer_class = ReservationSerializer


class CheckInAPIList(ListAPIView):
    queryset = CheckIn.objects
    serializer_class = CheckInSerializer
    permission_classes = [IsAdminUser]


class ReservationAPI(RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects
    serializer_class = ReservationSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser | ReadOnly]


class CheckInAPI(RetrieveUpdateDestroyAPIView):
    queryset = CheckIn.objects
    serializer_class = CheckInSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser | ReadOnly]


class RoomReservationsAPIList(ListAPIView):
    queryset = Reservation.objects
    serializer_class = ReservationSerializer

    def list(self, request, room_id, **kwargs):
        room = get_object_or_404(Room, id=room_id)
        queryset = self.queryset.filter(room=room)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomCheckInAPIList(RoomReservationsAPIList):
    queryset = CheckIn.objects
    serializer_class = CheckInSerializer


class SendMessageAPI(APIView):
    serializer_class = CreateMessageSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = Message.objects.create(author=request.user, text=serializer.data['text'])
        CheckIn.objects.filter(user=request.user).update(last_message_today=message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessagesAPIList(ListAPIView):
    queryset = Message.objects
    serializer_class = MessageSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, user_id, **kwargs):
        user = get_object_or_404(User, id=user_id)
        queryset = self.queryset.filter(author=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvgAllServicesAPI(APIView):
    serializer_class = AvgAllServices

    def get(self, request):
        type_services = TypeService.objects.all()
        avg_types_rate = Decimal(type_services.aggregate(avg_rate=Avg("avg_rate"))['avg_rate'])
        avg_types_rate = avg_types_rate.quantize(Decimal('1.00'))
        serializer = self.serializer_class(data={'avg_rate': avg_types_rate})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
