from django.urls import path

from hotel_api import views

app_name = "hotel-api"

urlpatterns = [
    path('', views.hello_api)
]