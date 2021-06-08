from django.contrib.auth.decorators import login_required
from django.urls import path

from hotel import views

app_name = "hotel"

urlpatterns = [
    path('admin-info/', views.admin_info, name='admin-info'),
    path('put_rate/<int:rate>/<int:type_id>/', views.put_a_rating, name='put-rate'),
    path('room/check-in/<int:room_id>/<int:reservation_id>', views.chek_in, name='check-in'),
    path('room/check-in/<int:room_id>', views.chek_in, name='check-in'),
    path('room/delete/<int:pk>', login_required(views.RoomDeleteView.as_view()), name='delete'),
    path('room/create/', login_required(views.RoomCreateView.as_view()), name='add'),
    path('room/edit/<int:pk>', login_required(views.RoomEditView.as_view()), name='edit'),
    path("room/<int:pk>", views.room_detail, name='detail'),
    path("room/reservation/<int:pk>", views.make_reservation, name='reservation'),
    path("", views.main_page, name='main'),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
]