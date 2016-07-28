from django.db import transaction
from django.utils.decorators import method_decorator
from datetime import datetime
from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.viewsets import DynamicModelViewSet, WithDynamicViewSetMixin
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from hotelBooking.auth.decorators import login_required_and_is_partner
from hotelBooking.core.order_creator.utils import add_hotel_order, generateHotelPackageProductOrder
from hotelBooking.core.utils.serializer_helpers import wrapper_response_dict
from hotelBooking.models import User, Hotel, Room, HotelPackageOrder
from hotelBooking.models.products import Product, RoomDayState
from hotelBooking.models.products import RoomPackage
from hotelBooking.models.ProductUtils import RoomPackageCreator
from hotelBooking.permissions.rolepermissions import IsHotelPartnerRole, CustomerPermission, PartnerPermission
from hotelBooking.serializers import CustomerOrderSerializer
from hotelBooking.serializers.products import RoomDayStateSerializer, RoomPackageSerializer
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse
from hotelBooking.utils.decorators import parameter_necessary
from hotelBooking.utils.dateutils import formatStrToDate

from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, detail_route, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from hotelBooking.views.viewsets import CustomViewSetMixin


class AddRoomPackageView(APIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.get(phone_number=15726814574)
        p = Product(owner=user)
        p.save()
        hp = RoomPackage(front_price=300, need_point=10, room=Room.objects.first(), product=p)
        hp.save()
        return Response(wrapper_response_dict(message='创建成功'))


"""
@api {post} /product/hoousepackage/?action=create
@apiName create new hotel package
@apiGroup partner 合作商户
@apiParam {hotelid} id of hte hotel model primary key.
@apiParm {frontPrice} front desk price
@apiParm {point}  need deducted the point
@apiParm {room} the room type like '豪华双床房'
@apiSuccess {String} firstname Firstname of the User.
@apiSuccess {String} lastname  Lastname of the User.
"""




class RoomPackageStateView(viewsets.ModelViewSet):
    serializer_class = RoomDayStateSerializer
    queryset = RoomDayState.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(wrapper_response_dict(serializer.data))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class RoomPackageView(CustomViewSetMixin,WithDynamicViewSetMixin, ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    serializer_class = RoomPackageSerializer
    queryset = RoomPackage.objects.all()


    def retrieve(self, request, *args, **kwargs):
        # hotel_query_utils.query(1,0,0)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(wrapper_response_dict(data=serializer.data))

    @method_decorator(permission_classes( (IsAuthenticated, PartnerPermission)))
    def create(self, request, *args, **kwargs):
        from hotelBooking.serializers.products import RoomPackageCreateSerialzer
        request_data = request.data.copy()
        request_data['owner'] = request.user.id
        serializer = RoomPackageCreateSerialzer(data=request_data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(wrapper_response_dict(message='创建成功审核中'))

    @detail_route(methods=['GET', 'POST'], url_path='book')
    @method_decorator(parameter_necessary('checkinTime', 'checkoutTime', 'guests', 'price_type'))
    def book(self, request, pk, checkinTime, checkoutTime, guests, price_type):
        print('_____开始预订')
        roomPackage = self.get_object()
        checkinTime = formatStrToDate(checkinTime)
        checkoutTime = formatStrToDate(checkoutTime)
        user = request.user
        from hotelBooking.validation import orderValidates
        if not orderValidates.validate_book_date(checkinTime, checkoutTime):
            return Response(wrapper_response_dict(code=-100, message='非法的check time'))
        exist = HotelPackageOrder.objects.filter(customer=request.user, checkin_time__lte=checkinTime,
                                                 checkout_time__gt=checkinTime, closed=False).exists()

        if (exist):
            return Response(wrapper_response_dict(code=-100, message='存在当天订单 请先取消'))

        request_notes = '需要wifi'
        # 内部检查了积分是否足够

        hotelPackageOrder = generateHotelPackageProductOrder(request, user, roomPackage, request_notes, checkinTime,
                                                             checkoutTime, price_type)
        serializer = CustomerOrderSerializer(hotelPackageOrder)
        return DefaultJsonResponse(res_data=serializer.data, message='预订成功')


    def get_serializer_class(self):
#     todo  通过判断请求方法 或者请求的地址提供不同的 serializser
        return self.serializer_class