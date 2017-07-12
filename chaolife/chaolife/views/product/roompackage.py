# -*- coding:utf-8 -*-
from django.db import transaction
from django.utils.decorators import method_decorator
from datetime import datetime
from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.viewsets import DynamicModelViewSet, WithDynamicViewSetMixin
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, detail_route, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from chaolife.core.utils.serializer_helpers import wrapper_response_dict
from chaolife.models import User, Hotel, Room, HotelPackageOrder
from chaolife.models.products import Product, RoomDayState
from chaolife.models.products import RoomPackage
from chaolife.models.ProductUtils import RoomPackageCreator
from chaolife.serializers import HotelOrderSerializer
from chaolife.serializers.products import RoomDayStateSerializer, RoomPackageSerializer
from chaolife.utils.AppJsonResponse import DefaultJsonResponse
from chaolife.views.viewsets import CustomSupportMixin
from chaolife.exceptions import ConditionDenied, PermissionDenied
from common.decorators import parameter_necessary, require_data

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
        return DefaultJsonResponse(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return DefaultJsonResponse(serializer.data)


class RoomPackageView(CustomSupportMixin, WithDynamicViewSetMixin,  ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = RoomPackageSerializer
    queryset = RoomPackage.canBookingProduct.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return DefaultJsonResponse(data=serializer.data)

    @detail_route(methods=['POST',], url_path='book',)
    @method_decorator(require_data('pay_pwd',))
    def book(self, request, pk,*args,**kwargs):
        from ...serializers.hotelorders.hotelorder import HotelOrderCreateSerializer
        data = request.data.copy()
        pay_pwd = data.pop('pay_pwd',None)[0]
        request.user.check_pay_pwd(pay_pwd)
        with transaction.atomic():
            s = HotelOrderCreateSerializer(data=data,context={'request':request,'roomPackage':self.get_object()})
            s.is_valid(raise_exception=True)
            s.save()
        return DefaultJsonResponse( {'order':s.data}, message='预订成功')

    def validate_customRoomName(self,hotelId, value):
        # todo 判断是否已经存在
        print('value is {}'.format(value))
        from chaolife.models import Room
        try:
            Hotel.objects.get(id=hotelId).hotel_rooms.get(name=value)
        except Room.DoesNotExist:
            from chaolife.models import Room
            room = Room(name=value, hotel_id=hotelId,)
            room.save()
            return room.id
        except Room.MultipleObjectsReturned:
            raise ConditionDenied(detail='房型名已经存在')
            # warn this is should be excepted
        else:
            raise ConditionDenied(detail='房型名已经存在')


    def get_serializer_class(self):
        #    todo  通过判断请求方法 或者请求的地址提供不同的 serializser
        return self.serializer_class





