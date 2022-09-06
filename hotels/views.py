from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Request, Response, status

from hotels.models import Hotel

from .permissions import IsOwnerUserPermission
from .serializers import HotelSerializer


class HotelViews(ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class HotelDetailsViews(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerUserPermission]
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    lookup_url_kwarg = "hotel_id"

    def delete(self, request, *args, **kwargs):
        address = request.user.address

        super().delete(request, *args, **kwargs)

        address.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
