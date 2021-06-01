from django.contrib import admin
from .models import Room, Reservation, CheckIn


admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(CheckIn)
