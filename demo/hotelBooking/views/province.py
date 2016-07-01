from hotelBooking.core.viewsets import GenericJsonViewSet
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response

from hotelBooking import Province
from hotelBooking.serializers import ProvinceSerializer
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse


class ProvinceViewSet(RetrieveModelMixin, GenericJsonViewSet):
    serializer_class = ProvinceSerializer
    queryset= Province.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_json_response(key='provinces',data=serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)