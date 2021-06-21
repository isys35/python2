from django.contrib.auth.decorators import login_required
from django.urls import path, include

from hotel import views

app_name = "hotel"

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path("login/", views.log_in, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('messages-history/<int:user_id>', views.messages_history, name='messages-history'),
    path('admin-info/', views.admin_info, name='admin-info'),
    path('room/check-in/<int:pk>/', views.chek_in, name='check-in'),
    path("room/reservation/<int:pk>", views.make_reservation, name='reservation'),
    path('room/delete/<int:pk>', views.delete_room_page, name='delete'),
    path('room/edit/<int:pk>', views.edit_room_page, name='edit'),
    path("room/<int:pk>", views.detail_room_page, name='detail'),
    path('room/create/', views.create_room_page, name='add'),
    path("", views.main_page, name='main'),
]
