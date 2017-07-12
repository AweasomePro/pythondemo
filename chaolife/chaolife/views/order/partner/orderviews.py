from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework_extensions.mixins import DetailSerializerMixin

from chaolife.pagination import StandardResultsSetPagination
from chaolife.utils.AppJsonResponse import DefaultJsonResponse
from chaolife.utils.decorators import parameter_necessary
from dynamic_rest.viewsets import DynamicModelViewSet, WithDynamicViewSetMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from rest_framework import filters
from chaolife.models.orders import Order, HotelPackageOrder
from chaolife.permissions.rolepermissions import PartnerPermission
from chaolife.serializers.orders import OrderSerializer, HotelOrderSerializer, HotelOrderDetailSerializer
from chaolife.service import HotelOrderOperationService
from sms.tasks import notify_reservation_update
import logging

# Get an instance of a logger
from common.viewsets import CustomSupportMixin

logger = logging.getLogger(__name__)


# from logging import l
class PartnerHotelOrderViewSet(CustomSupportMixin, DetailSerializerMixin, DynamicModelViewSet):
    # warn  用户可能会通过 post 请求直接创建订单，这是不被允许的，所以需要调整该viewset 不允许post 请求提交对象
    permission_classes = (IsAuthenticated, PartnerPermission)
    queryset = HotelPackageOrder.objects.all()
    serializer_detail_class = HotelOrderDetailSerializer
    serializer_class = HotelOrderSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('process_state', 'closed', 'checkin_time', 'checkout_time')
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

    #  api like
    @method_decorator(parameter_necessary('action', ))
    @detail_route(methods=['GET', 'POST'], url_path='handle')
    def handle_order(self, request, number=None, action=None, *args, **kwargs):
        """
        :param request:
        :param number: 订单号
        :return:
        """
        hotel_order = self.get_object()
        service = HotelOrderOperationService(hotel_order, request.user)
        if (action == 'refuse'):
            service.cancel_book(commit=True)
            # succeess, code = hotel_order.refuse_by(request.user)
        elif (action == 'accept'):
            service.accept_book()
        else:
            return DefaultJsonResponse(message='位置的操作', )
        hotel_order.refresh_from_db()
        s_class = self.get_serializer_class()
        serializer = s_class(hotel_order)
        return DefaultJsonResponse(message='处理成功', data={'order': serializer.data})

    @detail_route(methods=['PATCH', ], url_path='reservation-number')
    def write_reservation_number(self, request, number=None, ):
        hotelPackageOrder = self.get_object()
        reservation_number = request.data.get('reservation_number')
        hotelPackageOrder.reservation_number = reservation_number
        hotelPackageOrder.save(update_fields=('reservation_number',))
        customer = hotelPackageOrder.customer
        notify_reservation_update.delay(customer.phone_number, customer.name, hotelPackageOrder.checkin_time,
                                  hotelPackageOrder.checkout_time, hotelPackageOrder, hotelPackageOrder.hotel_name,
                                  reservation_number)
        return DefaultJsonResponse('添加预订号成功')

    def get_queryset(self, queryset=None):
        return self.queryset.filter(seller=self.request.user)
