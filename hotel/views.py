from django.shortcuts import render
from .models import Room


def main_page(requests):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(requests, 'hotel/index.html', context=context)


def room_detail(request, pk):
    room = Room.objects.get(pk=pk)
    context = {'room': room}
    return render(request, 'hotel/room.html', context=context)