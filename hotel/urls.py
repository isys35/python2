from django.urls import path

from hotel import views

app_name = "hotel"

urlpatterns = [
    path('room/create/', views.RoomCreateView.as_view(), name='add'),
    path('room/edit/<int:pk>', views.RoomEditView.as_view(), name='edit'),
    path("room/<int:pk>", views.room_detail, name='detail'),
    path("", views.main_page, name='main'),
]