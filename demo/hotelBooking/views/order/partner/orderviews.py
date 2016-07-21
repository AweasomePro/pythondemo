from django.utils.decorators import method_decorator
from rest_framework.response import Response

from hotelBooking.core.utils.serializer_helpers import wrapper_response_dict
from hotelBooking.utils.decorators import parameter_necessary
from hotelBooking.views import views,viewsets
from dynamic_rest.viewsets import DynamicModelViewSet,WithDynamicViewSetMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route,list_route
from rest_framework import filters
from hotelBooking.models.orders import Order,HotelPackageOrder
from hotelBooking.permissions.rolepermissions import PartnerPermission
from hotelBooking.serializers.orders import OrderSerializer, PartnerHotelPackageOrderSerializer
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# from logging import l
class PartnerHotelOrderViewSet(DynamicModelViewSet):
    permission_classes = (IsAuthenticated,PartnerPermission)
    queryset = HotelPackageOrder.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields =('process_state','closed','checkin_time')
    lookup_field = 'number'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            print('to page')
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    #  api like
    @detail_route(methods=['GET','POST'],url_path='handle')
    @method_decorator(parameter_necessary('action',))
    def handle_order(self,request,number=None, action=None, *args,**kwargs):
        """
        :param request:
        :param number: 订单号
        :return:
        """
        hotel_order = self.get_object()
        if(action == 'refuse'):
            succeess, code = hotel_order.refuse_by(request.user)
            if succeess:
                return Response('处理成功')
            else:
                return Response(wrapper_response_dict(message=code,code=-100))

        if (action == 'accept'):
            succeess, code =hotel_order.accept_by(request.user)
            if succeess:
                return Response('处理成功')
            else:
                return Response(wrapper_response_dict(message=code, code=-100))
        return Response('success')


    def get_serializer_class(self,*args,**kwargs):
        return PartnerHotelPackageOrderSerializer

    def get_queryset(self, queryset=None):
        self.queryset.filter(product__owner=self.request.user)

