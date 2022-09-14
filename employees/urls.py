from django.urls import path

from . import views

urlpatterns = [
    path("employees/", views.EmployeeView.as_view(), name="list-create-employee"),
    path("employees/<str:employee_id>/", views.EmployeeDetailView.as_view(), name="list-create-detail-employee"),
]
