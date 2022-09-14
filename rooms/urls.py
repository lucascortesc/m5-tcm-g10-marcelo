from django.urls import path

from rooms.views import RoomDetailView, RoomView

urlpatterns = [
    path("rooms/", RoomView.as_view()),
    #path("rooms/filter/", RoomFilterView.as_view()),
    path("rooms/<str:room_id>/", RoomDetailView.as_view()),

]
