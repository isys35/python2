from django.forms import ModelForm
from django import forms

from hotel.models import Room, Reservation


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'floor', 'number_of_rooms', 'description', 'room_class']


class ReservationForm(ModelForm):
    started_at = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

    class Meta:
        model = Reservation
        fields = ['description', 'started_at', 'ended_at']
