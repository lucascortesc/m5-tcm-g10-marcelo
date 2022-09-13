from django.urls import path

from . import views

urlpatterns = [
    path("hotels/", views.HotelViews.as_view()),
    path("hotels/<str:hotel_id>/", views.HotelDetailsViews.as_view()),
    path("hotels/amenities/<str:amenity_id>/", views.AmenitiesHotelViews.as_view()),
]
