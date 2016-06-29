from rest_framework import viewsets

from hotelBooking import HousePackage
from hotelBooking.serializers import HousePackageSerializer


class HousePackageViewSet(viewsets.GenericViewSet):
    serializer_class = HousePackageSerializer
    queryset = HousePackage.objects.all()

