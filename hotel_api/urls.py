from django.urls import path

from hotel_api import views

app_name = "hotel-api"

urlpatterns = [
    path('rooms/', views.RoomAPIList.as_view()),
    path('rooms/<int:pk>', views.RoomAPI.as_view()),
    path('services/', views.TypeServiceAPIList.as_view()),
    path('put_rate_service/<int:type_id>', views.MarkTypeServiceAPI.as_view()),
    path('create_reservation/<int:room_id>', views.CreateReservationAPI.as_view()),
    path('create_checkin/<int:room_id>/', views.CreateCheckInAPI.as_view()),
    path('avg_rate/', views.AvgRateAPI.as_view())
]