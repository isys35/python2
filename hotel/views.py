from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView


from .forms import RoomForm
from .models import Room


def main_page(requests):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(requests, 'hotel/index.html', context=context)


def room_detail(request, pk):
    room = Room.objects.get(pk=pk)
    context = {'room': room}
    return render(request, 'hotel/room.html', context=context)


class RoomEditView(UpdateView):
    model = Room
    form_class = RoomForm

    def get_success_url(self):
        return reverse_lazy('hotel:detail',
                            kwargs={'pk': self.object.pk})


class RoomCreateView(CreateView):
    template_name = 'hotel/create_room.html'
    form_class = RoomForm
    success_url = reverse_lazy('hotel:main')