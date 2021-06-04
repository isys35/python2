from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from datetime import datetime

from .forms import RoomForm, ReservationForm
from .models import Room, Reservation, CheckIn


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
    reservations = Reservation.objects.filter(room_id=pk)
    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            reservation = reservation_form.save(commit=False)
            reservation.user = request.user
            reservation.room_id = pk
            intersections_of_dates = Reservation.objects.filter(
                Q(started_at__gte=reservation.started_at, ended_at__lte=reservation.ended_at) |
                Q(started_at__lte=reservation.started_at, ended_at__gte=reservation.ended_at) |
                Q(started_at__gte=reservation.started_at, started_at__lte=reservation.ended_at,
                  ended_at__gte=reservation.ended_at) |
                Q(ended_at__gte=reservation.started_at, ended_at__lte=reservation.ended_at,
                  started_at__lte=reservation.ended_at)
            ).filter(room_id=pk)
            if intersections_of_dates:
                context = {'form': reservation_form, 'reservations': reservations, 'error_date': True}
                return render(request, "hotel/reservation_form.html", context)
            reservation.save()
            reservation_form.save_m2m()
            return redirect('hotel:detail', pk)
        else:
            context = {'form': reservation_form, 'reservations': reservations}
            return render(request, "hotel/reservation_form.html", context)
    reservation_form = ReservationForm()
    context = {'form': reservation_form, 'reservations': reservations}
    return render(request, "hotel/reservation_form.html", context)


@login_required
def chek_in(request: WSGIRequest, room_id, reservation_id=None):
    if request.method == 'POST':
        tenant_username = request.POST.get('username')
        tenant = User.objects.get(username=tenant_username)
        started_at = datetime.strptime(request.POST['started_at'], "%Y-%m-%d")
        ended_at = datetime.strptime(request.POST['ended_at'], "%Y-%m-%d")
        CheckIn.objects.create(
            user=tenant,
            started_at=started_at,
            ended_at=ended_at,
            room_id=room_id
        )
        return redirect('hotel:detail', room_id)
    reservations = Reservation.objects.filter(room_id=room_id)
    context = {'room': Room.objects.get(pk=room_id), 'reservations': reservations}
    if reservation_id:
        context['used_reservation'] = Reservation.objects.get(id=reservation_id)
    return render(request, "hotel/check_in_form.html", context)
