from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response

from hotelBooking import City
from hotelBooking.serializers import CitySerializer
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse


class CityViewSet(RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CitySerializer
    queryset= City.objects.all()

    def get(self, request):
        provinces = City.objects.all()
        serializer_provinces = CitySerializer(provinces, many=True)
        data = {'citys': serializer_provinces.data,}
        return DefaultJsonResponse(res_data=data, )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)