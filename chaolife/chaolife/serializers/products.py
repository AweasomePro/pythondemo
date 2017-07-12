#-*- coding: utf-8 -*-
import datetime
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from drf_enum_field.serializers import EnumFieldSerializerMixin
from dynamic_rest.fields import DynamicMethodField, DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer
# class
from common import appcodes
from ..models.hotel import Room, Hotel
from chaolife.models.products import RoomPackage, RoomDayState, Product
from chaolife.exceptions import ConditionDenied
class RoomDayStateSerializer(DynamicModelSerializer):

    class Meta:
        name = 'daystate'
        model = RoomDayState
        fields = ('id','s_point','s_price','d_point','d_price','date','state',)


class ProductSerializer(DynamicModelSerializer):
    class Meta:
        model = Product


class RoomPackageSerializer(EnumFieldSerializerMixin , DynamicModelSerializer):

    roomstates = RoomDayStateSerializer(many=True,embed=True)

    class Meta(ProductSerializer.Meta):
        model = RoomPackage
        fields = ('id','active','roomstates','breakfast','bill','deleted')


class PartnerRoomPackageSerializer(EnumFieldSerializerMixin , DynamicModelSerializer):

    roomstates = RoomDayStateSerializer(many=True,embed=True,read_only=True)

    class Meta():
        model = RoomPackage


class RoomPackageCreateSerializer(serializers.ModelSerializer):
    customRoomName = serializers.CharField(write_only=True,allow_blank=True)

    class Meta(ProductSerializer.Meta):
        model = RoomPackage
        read_only_fields =('checked','active',)

    def __init__(self,instance = None,data = None,context = None,**kwargs):
        room = Room.objects.select_related('hotel','hotel__city').get(id= data['room'])
        data['hotel_name'] = room.hotel.name
        data['room_name'] = room.name
        data['city']= room.hotel.city.code
        super(RoomPackageCreateSerializer,self).__init__(instance = instance,data = data,context = context,**kwargs)

    def validate(self, attrs):
        hotel = attrs.get('hotel')
        room = attrs.get('room')
        if not room.hotel_id == hotel.id:
            raise serializers.ValidationError('参数验证错误，该房型不属于该酒店,请联系')
        if attrs.get('default_d_price') < 100 or attrs.get('default_s_price')<100:
            raise ConditionDenied('房价过低,至少100',code=appcodes.CODE_THE_PRICE_IS_TO_LOW)
        #todo warn 判断这个 room 确实是对应的hotel
        request = self.context.get('request')
        user = request.user
        if (RoomPackage.objects.filter(owner =user, deleted = False,room = room, breakfast=attrs['breakfast']).exists()):
            raise ConditionDenied(detail='存在相同类型的房间,不能重复创建',code=appcodes.CODE_EXIST_SAME_PRODUCT)
        return attrs


    def check_exist_same_type_product(self,attrs):
        # from
        pass

    def create(self,validate_data):
        del validate_data['customRoomName']
        obj = super(RoomPackageCreateSerializer,self).create(validate_data)
        return obj


class ModifyRoomStateSerializer(serializers.Serializer):

    def __init__(self,data = None):
        super(ModifyRoomStateSerializer,self).__init__(instance=None,data=data)

