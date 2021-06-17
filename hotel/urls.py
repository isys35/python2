from django.contrib.auth.decorators import login_required
from django.urls import path, include

from hotel import views

app_name = "hotel"

urlpatterns = [
    path('avg_rate/', views.avg_rate),
    path('profile/', views.profile, name='profile'),
    path('messages-history/<int:user_id>', views.messages_history, name='messages-history'),
    path('admin-info/', views.admin_info, name='admin-info'),
    path('put_rate/', views.put_a_rating),
    path('room/check-in/<int:room_id>/<int:reservation_id>', views.chek_in, name='check-in'),
    path('room/check-in/<int:room_id>', views.chek_in, name='check-in'),
    path("room/reservation/<int:pk>", views.make_reservation, name='reservation'),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('room/delete/<int:pk>', views.delete_room_page, name='delete'),
    path('room/edit/<int:pk>', views.edit_room_page, name='edit'),
    path("room/<int:pk>", views.detail_room_page, name='detail'),
    path('room/create/', views.create_room_page, name='add'),
    path("", views.main_page, name='main'),
]
