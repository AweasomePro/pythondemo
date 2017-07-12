# -*- coding:utf-8 -*-
from dynamic_rest.viewsets import WithDynamicViewSetMixin
from rest_framework.viewsets import ReadOnlyModelViewSet
from chaolife.models.city import City
from chaolife.serializers import CitySerializer
from chaolife.utils.AppJsonResponse import DefaultJsonResponse
from common import fixutils

from common.viewsets import CustomSupportMixin
from chaolife.tasks import notify_partner,notify_customer
import datetime
class CityViewSet(CustomSupportMixin,WithDynamicViewSetMixin,ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    queryset= City.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        fixutils.fix_installtion_channels()
        return DefaultJsonResponse(data=serializer.data,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.POST.get('page'):
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return DefaultJsonResponse(data=serializer.data)

