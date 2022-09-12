from employees.permissions import IsAuthenticatedOrAdmin
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

from guests.permissions import RetrieveGuestPermissions

from .models import Guest
from .serializers import GuestSerializer


class GuestView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrAdmin]

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def perform_create(self, serializer):
        serializer.save(hotel=self.request.user)


class RetrieveGuestView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [RetrieveGuestPermissions]

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    lookup_url_kwarg = "guest_id"
