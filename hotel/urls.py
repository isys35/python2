from django.urls import path

from hotel import views

app_name = "hotel"

urlpatterns = [
    path("room/<int:pk>", views.room_detail, name='detail'),
    path("", views.main_page),
]