from django.urls import path

from . import views

urlpatterns = [
    path("employees/", views.EmployeeView.as_view()),
    path("employees/<str:employee_id>/", views.EmployeeDetailView.as_view()),
]
