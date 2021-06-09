from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q, Avg, Count, Prefetch, Subquery, OuterRef
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import UpdateView, CreateView, DeleteView
import datetime
from rest_framework import generics

from rest_framework import viewsets

from .forms import RoomForm, ReservationForm
from .models import Room, Reservation, CheckIn, TypeService, UserTypeService, Message
from .serializers import TypeServiceSerializer
from .utils import get_intersections


def main_page(requests: WSGIRequest) -> HttpResponse:
    rooms = Room.objects.all()
    type_services = TypeService.objects.prefetch_related('rated_type_service').all()
    avg_types_rate = type_services.aggregate(avg_rate=Avg("avg_rate"))['avg_rate']
    context = {'rooms': rooms, 'type_services': type_services, 'avg_types_rate': avg_types_rate}
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
            intersections_of_dates = get_intersections(reservation)
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
        started_at = datetime.datetime.strptime(request.POST['started_at'], "%Y-%m-%d")
        ended_at = datetime.datetime.strptime(request.POST['ended_at'], "%Y-%m-%d")
        chek_in = CheckIn(
            user=tenant,
            started_at=started_at,
            ended_at=ended_at,
            room_id=room_id
        )
        intersections_of_dates = get_intersections(chek_in)
        if intersections_of_dates:
            return redirect("hotel:check-in", room_id)
        chek_in.save()
        return redirect('hotel:detail', room_id)
    reservations = Reservation.objects.filter(room_id=room_id)
    context = {'room': Room.objects.get(pk=room_id), 'reservations': reservations}
    if reservation_id:
        context['used_reservation'] = Reservation.objects.get(id=reservation_id)
    return render(request, "hotel/check_in_form.html", context)


@login_required
@require_http_methods(["POST"])
def put_a_rating(request: WSGIRequest):
    type_id = request.POST['type_service_id']
    rate = request.POST['rate']
    UserTypeService.objects.update_or_create(
        user_id=request.user.id,
        type_service_id=type_id,
        defaults={"rate": rate}
    )
    ts = TypeService.objects.get(id=type_id)
    ts.avg_rate = ts.rated_type_service.aggregate(rate=Avg("rate"))['rate']
    ts.count_rate = ts.users.count()
    ts.save(update_fields=['avg_rate', 'count_rate'])
    serializer = TypeServiceSerializer(ts)
    return JsonResponse(serializer.data, safe=False)


@staff_member_required
def admin_info(request: WSGIRequest):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    sq = Subquery(Message.objects.filter(author_id=OuterRef('user_id'),
                                         pub_date__gte=today,
                                         pub_date__lt=tomorrow).values('text')[:1])
    sq2 = Subquery(Message.objects.filter(author_id=OuterRef('user_id'),
                                          pub_date__gte=today,
                                          pub_date__lt=tomorrow).values('pub_date')[:1])
    chek_ins = CheckIn.objects.select_related().annotate(last_message=sq, last_message_date=sq2).all()
    context = {'chek_ins': chek_ins}
    return render(request, "hotel/admin-info.html", context=context)


@staff_member_required
def messages_history(request: WSGIRequest, user_id: int):
    messages = Message.objects.filter(author_id=user_id).order_by('pub_date')
    author = User.objects.get(id=user_id)
    context = {'messages': messages, 'author': author}
    return render(request, "hotel/messages-history.html", context=context)


@login_required
def profile(request: WSGIRequest):
    if request.method == 'POST':
        text = request.POST['text']
        Message.objects.create(author=request.user, text=text)
        return redirect('hotel:profile')
    messages = Message.objects.filter(author_id=request.user.id).order_by('pub_date')
    context = {'messages': messages}
    return render(request, "hotel/profile.html", context=context)


class TypeServiceListAPI(generics.ListAPIView):
    queryset = TypeService.objects.all()
    serializer_class = TypeServiceSerializer

