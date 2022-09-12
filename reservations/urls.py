from django.urls import path

from . import views

urlpatterns = [
    path("rooms/<str:room_id>/reservations/", views.ReservationView.as_view()),
    path("reservations/<str:reservation_id>/", views.RetrieveReservationView.as_view()),
]
