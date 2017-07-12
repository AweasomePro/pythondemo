# -*- coding:utf-8 -*-
from datetime import datetime

from django.db import transaction
from django.utils.decorators import method_decorator
from dynamic_rest.viewsets import WithDynamicViewSetMixin

from rest_framework import filters
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from authtoken.authentication import TokenAuthentication
from chaolife.models.orders import HotelPackageOrder, HotelPackageOrderItem,Order
from chaolife.pagination import StandardResultsSetPagination
from chaolife.serializers import HotelOrderSerializer
from chaolife.utils.AppJsonResponse import DefaultJsonResponse
from chaolife.service import HotelOrderOperationService
from account.decorators import only_customer
from common.viewsets import CustomSupportMixin
from dynamic_rest.filters import DynamicFilterBackend
from common.permissions.orderpermissions import IsOrderCustomer

class CustomerHotelBookOrderList(CustomSupportMixin,WithDynamicViewSetMixin,ModelViewSet):

    permission_classes = (IsAuthenticated,)
    queryset = HotelPackageOrder.objects.all()
    serializer_class = HotelOrderSerializer
    filter_backends = (filters.DjangoFilterBackend,DynamicFilterBackend)
    filter_fields =('process_state','closed','checkin_time')
    lookup_field = 'number'
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            print('to page')
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return DefaultJsonResponse(serializer.data)

    @method_decorator(only_customer)
    @detail_route(methods=['GET','POST'], url_path='cancel')
    def handle_order(self, request, number=None, *args, **kwargs):
        """
        :param request:
        :param number: 订单号
        :return:
        """
        # 在ios 端，GET请求无法取到token?????????? ,so 加了 post......
        with transaction.atomic():
            order = self.get_object()
            service = HotelOrderOperationService(order,request.user)
            service.cancel_book(commit=True)
            order.refresh_from_db()
            cs = HotelOrderSerializer(order)
            return DefaultJsonResponse(message='退订成功', data={'order':cs.data})

    @detail_route(methods=['PUT',], url_path='refund',permission_classes=[IsOrderCustomer])
    def refund_order(self,request,*args,**kwargs):
        order = self.get_object()
        return DefaultJsonResponse(message='退款请求成功',)

    def get_queryset(self,queryset=None):
        queryset = self.queryset
        user = self.request.user
        print(self.request.query_params)
        if(self.request._request.path.endswith('cancel/')):
            print('yes get its')
            queryset.select_for_update().prefetch_related('seller','customer').filter(customer=user)
        return queryset.filter(customer=user)







