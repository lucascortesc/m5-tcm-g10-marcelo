from django.urls import path

from . import views

urlpatterns = [
    path("guests/", views.GuestView.as_view()),
    path("guests/<pk>/", views.RetrieveGuestView.as_view())
]
