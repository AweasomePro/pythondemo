from datetime import datetime

from django.db import transaction
from django.utils.decorators import method_decorator
from dynamic_rest.viewsets import WithDynamicViewSetMixin
from guardian.core import ObjectPermissionChecker
from guardian.shortcuts import assign_perm
from rest_framework import filters
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import detail_route
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication

from hotelBooking.core.utils.serializer_helpers import wrapper_response_dict
from hotelBooking.exceptions import PointNotEnough, ConditionDenied
from hotelBooking.models.orders import HotelPackageOrder, HotelPackageOrderItem
from hotelBooking.models.plugins import HotelOrderNumberGenerator
from hotelBooking.models.products import RoomPackage
from hotelBooking.pagination import StandardResultsSetPagination
from hotelBooking.serializers import CustomerOrderSerializer
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse, JSONWrappedResponse
from hotelBooking.utils.decorators import parameter_necessary

class CustomerHotelBookOrderList(WithDynamicViewSetMixin,ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = HotelPackageOrder.objects.all()
    serializer_class = CustomerOrderSerializer
    filter_backends = (filters.DjangoFilterBackend,)
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
        return JSONWrappedResponse(serializer.data)

    @detail_route(methods=['GET','POST'], url_path='cancel')
    def handle_order(self, request, number=None, *args, **kwargs):
        """
        :param request:
        :param number: 订单号
        :return:
        """
        order = self.get_object()
        checker = ObjectPermissionChecker(request.user)
        # print(checker.has_perm('hotelpackageorder.change_process_state', order))
        #  用户取消订单
        success, order = order.customer_cancel_order(request.user)
        if (success):
            order.refresh_from_db()
        cs = CustomerOrderSerializer(order)
        return Response(wrapper_response_dict(message='退订成功', data={'order':cs.data}))





    def get_queryset(self,queryset=None):
        queryset = self.queryset
        user = self.request.user
        state = self.request.GET.get('state')
        return queryset.filter(customer=user)

# url is  order/customer
class CustomerOrderActionAPIView(WithDynamicViewSetMixin,ModelViewSet):
    serializer_class = CustomerOrderSerializer
    queryset = HotelPackageOrder.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    ACTION_CANCEL = 'cancel'

    def post(self,request):
        action = request.POST.get('action',None)
        number = request.POST.get('number', None)
        if number:
            request.number = number
            try:
                order = HotelPackageOrder.objects.get(number=number)
                request.order = order
                print('request user is {}'.format(request.user.name))
                print('order customer is {}'.format(request.order.customer))
            except HotelPackageOrder.DoesNotExist:
                return Response('error number')

        checker = ObjectPermissionChecker(request.user)
        print(checker.has_perm('hotelpackageorder.change_process_state', order))
        if action == CustomerOrderActionAPIView.ACTION_CANCEL:
            #  用户取消订单
            hotelpackageorder = request.order  #用get_object代替
            success,order = request.order.customer_cancel_order(request.user)
            if(success):
                order.refresh_from_db()
            cs = CustomerOrderSerializer(hotelpackageorder)
            return Response(wrapper_response_dict(message='退订成功',data=cs.data))
        else:
            return Response(data='未知操作')



