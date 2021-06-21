from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect


def main_page(requests: WSGIRequest) -> HttpResponse:
    return render(requests, 'hotel/index.html')


@staff_member_required
def create_room_page(requests: WSGIRequest) -> HttpResponse:
    return render(requests, 'hotel/create_room.html')


def detail_room_page(request: WSGIRequest, pk: int) -> HttpResponse:
    context = {'room_pk': pk}
    return render(request, 'hotel/room.html', context=context)


@staff_member_required
def edit_room_page(request: WSGIRequest, pk: int) -> HttpResponse:
    context = {'room_pk': pk}
    return render(request, 'hotel/room_form.html', context=context)


@staff_member_required
def delete_room_page(request: WSGIRequest, pk: int) -> HttpResponse:
    context = {'room_pk': pk}
    return render(request, 'hotel/room_confirm_delete.html', context=context)


@login_required
def make_reservation(request: WSGIRequest, pk: int) -> HttpResponse:
    context = {'room_pk': pk}
    return render(request, "hotel/reservation_form.html", context)


@staff_member_required
def chek_in(request: WSGIRequest, pk: int) -> HttpResponse:
    context = {'room_pk': pk}
    return render(request, "hotel/check_in_form.html", context)


@staff_member_required
def admin_info(request: WSGIRequest) -> HttpResponse:
    return render(request, "hotel/admin-info.html")


@staff_member_required
def messages_history(request: WSGIRequest, user_id: int) -> HttpResponse:
    context = {'user_id': user_id}
    return render(request, "hotel/messages-history.html", context=context)


@login_required
def profile(request: WSGIRequest) -> HttpResponse:
    return render(request, "hotel/profile.html")


def log_in(request: WSGIRequest) -> HttpResponse:
    return render(request, "hotel/login.html")


def logout_view(request: WSGIRequest):
    logout(request)
    return redirect("hotel:main")
