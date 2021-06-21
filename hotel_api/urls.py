from django.urls import path

from hotel_api import views

app_name = "hotel-api"

urlpatterns = [
    path('rooms/', views.RoomAPIList.as_view(), name='rooms'),
    path('room-create/', views.CreateRoomAPI.as_view(), name='create-room'),
    path('rooms/<int:pk>', views.RoomAPI.as_view(), name='room-detail'),
    path('services/', views.TypeServiceAPIList.as_view()),
    path('put_rate_service/', views.PutRateTypeServiceAPI.as_view(), name='put-rate'),
    path('create_reservation/', views.CreateReservationAPI.as_view(), name='create-reservation'),
    path('create_checkin/', views.CreateCheckInAPI.as_view(), name='create-checkin'),
    path('reservations/', views.ReservationAPIList.as_view()),
    path('checkins/', views.CheckInAPIList.as_view(), name="check-ins"),
    path('reservations/<int:pk>', views.ReservationAPI.as_view()),
    path('checkins/<int:pk>', views.CheckInAPI.as_view()),
    path('room_reservations/<int:room_id>', views.RoomReservationsAPIList.as_view(), name='room-reservations'),
    path('room_checkins/<int:room_id>', views.RoomCheckInAPIList.as_view()),
    path('send_message/', views.SendMessageAPI.as_view(), name='send-message'),
    path('messages/<int:user_id>', views.MessagesAPIList.as_view(), name='message-history'),
    path('avg-rate-all-services/', views.AvgAllServicesAPI.as_view(), name='avg-rate-all-services'),
    path('login/', views.LoginAPI.as_view(), name='login')
]