from hotelBooking.models.city import City
from hotelBooking.serializers import CitySerializer
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse
from rest_framework import viewsets
from rest_framework.mixins import RetrieveModelMixin


class CityViewSet(RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CitySerializer
    queryset= City.objects.all()

    def get(self, request, *args, **kwargs):
        provinces = City.objects.all()
        serializer_provinces = CitySerializer(provinces, many=True)
        data = {'citys': serializer_provinces.data,}
        return DefaultJsonResponse(res_data=data, )
