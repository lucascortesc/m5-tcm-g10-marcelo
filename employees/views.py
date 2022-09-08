from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from employees.models import Employee
from employees.serializers import EmployeeDetailSerializer, EmployeeSerializer

from .mixins import SerializerByMethodMixin
from .permissions import IsAuthenticatedOrAdmin


class EmployeeView(SerializerByMethodMixin, ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrAdmin]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    serializer_map = {
        "POST": EmployeeDetailSerializer,
        "GET": EmployeeSerializer
    }

    def perform_create(self, serializer):
        serializer.save(hotel=self.request.user)
    

class EmployeeDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrAdmin]
    queryset = Employee.objects.all()
    serializer_class = EmployeeDetailSerializer
    lookup_url_kwarg = "employee_id"
