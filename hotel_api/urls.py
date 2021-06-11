from django.urls import path

from hotel_api import views

app_name = "hotel-api"

urlpatterns = [
    path('rooms/', views.RoomAPIList.as_view()),
    path('rooms/<int:pk>', views.RoomAPI.as_view()),
    path('services/', views.TypeServiceAPIList.as_view()),
    path('put_rate_service/<int:type_id>', views.MarkTypeService.as_view())
]