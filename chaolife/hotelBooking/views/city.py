from rest_framework import viewsets
from rest_framework.mixins import RetrieveModelMixin
from dynamic_rest.serializers import WithDynamicModelSerializerMixin,DynamicModelSerializer
from dynamic_rest.viewsets import DynamicModelViewSet
from hotelBooking.models.city import City
from hotelBooking.serializers import CitySerializer
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse
from hotelBooking.serializers.products import RoomDayStateSerializer
from hotelBooking.models import RoomDayState

class CityViewSet(DynamicModelViewSet):
    serializer_class = CitySerializer
    queryset= City.objects.all()

    def get(self, request, *args, **kwargs):
        citys = City.objects.all()
        serializer_provinces = CitySerializer(citys, many=True)
        data = {'citys': serializer_provinces.data,}
        return DefaultJsonResponse(res_data=data, )
