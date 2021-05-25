from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from .forms import RoomForm, ReservationForm
from .models import Room, Reservation


def main_page(requests: WSGIRequest) -> HttpResponse:
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(requests, 'hotel/index.html', context=context)


def room_detail(request: WSGIRequest, pk: int) -> HttpResponse:
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


class RoomDeleteView(DeleteView):
    model = Room
    success_url = reverse_lazy('hotel:main')


class LoginView(View):
    def get(self, request: WSGIRequest) -> HttpResponse:
        return render(request, "hotel/login.html")

    def post(self, request: WSGIRequest) -> HttpResponse:
        user = authenticate(
            username=request.POST['login'],
            password=request.POST['pwd']
        )
        if user is not None:
            login(request, user)
            return redirect("hotel:main")
        return redirect("hotel:login")


def logout_view(request: WSGIRequest):
    logout(request)
    return redirect("hotel:main")


@login_required
def make_reservation(request: WSGIRequest, pk):
    room = Room.objects.get(pk=pk)
    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            reservation = reservation_form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            reservation_form.save_m2m()
            return redirect('hotel:main')
        else:
            context = {'form': reservation_form, 'room': room}
            return render(request, "hotel/reservation_form.html", context)
    reservation_form = ReservationForm()
    context = {'form': reservation_form, 'room': room}
    return render(request, "hotel/reservation_form.html", context)