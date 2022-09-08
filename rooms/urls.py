from django.urls import path

from rooms.views import RoomDetailView, RoomView


urlpatterns = [
    path("hotels/rooms/", RoomView.as_view()),
    path("hotels/rooms/<str:room_id>/", RoomDetailView.as_view()),
]
