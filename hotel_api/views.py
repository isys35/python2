from rest_framework import status
from rest_framework.response import Response

from hotel.models import Room, TypeService, UserTypeService
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, \
    UpdateAPIView
from rest_framework.permissions import IsAdminUser, BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from hotel_api.serializers import RoomSerializer, TypeServiceSerializer, UserTypeServiceSerializer


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


class MarkTypeService(CreateAPIView):
    queryset = UserTypeService.objects
    serializer_class = UserTypeServiceSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
