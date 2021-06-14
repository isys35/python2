from django.urls import path

from hotel_api import views

app_name = "hotel-api"

urlpatterns = [
    path('rooms/', views.RoomAPIList.as_view()),
    path('rooms/<int:pk>', views.RoomAPI.as_view()),
    path('services/', views.TypeServiceAPIList.as_view()),
    path('put_rate_service/', views.PutRateTypeServiceAPI.as_view()),
    path('create_reservation/', views.CreateReservationAPI.as_view()),
    path('create_checkin/', views.CreateCheckInAPI.as_view()),
    # path('avg_rate/', views.AvgRateAPI.as_view())
]