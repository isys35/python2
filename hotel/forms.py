from django.forms import ModelForm
from django import forms

from hotel.models import Room, Reservation


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'floor', 'number_of_rooms', 'description', 'room_class']


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['description', 'started_at', 'ended_at']