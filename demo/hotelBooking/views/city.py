from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response

from hotelBooking import City
from hotelBooking.core.serializers.city import CitySerializer
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse


class CityViewSet(RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CitySerializer
    queryset= City.objects.all()

    def get(self, request):
        provinces = City.objects.all()
        serializer_provinces = CitySerializer(provinces, many=True)
        data = {'citys': serializer_provinces.data,}
        return DefaultJsonResponse(res_data=data, )
