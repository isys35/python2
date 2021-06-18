from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

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
def messages_history(request: WSGIRequest, user_id: int)-> HttpResponse:
    context = {'user_id': user_id}
    return render(request, "hotel/messages-history.html", context=context)


@login_required
def profile(request: WSGIRequest)-> HttpResponse:
    return render(request, "hotel/profile.html")


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

# @login_required
# def profile(request: WSGIRequest):
#     if request.method == 'POST':
#         text = request.POST['text']
#         Message.objects.create(author=request.user, text=text)
#         return redirect('hotel:profile')
#     messages = Message.objects.filter(author_id=request.user.id).order_by('pub_date')
#     context = {'messages': messages}
#     return render(request, "hotel/profile.html", context=context)
