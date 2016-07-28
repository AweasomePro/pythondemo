import datetime
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from drf_enum_field.serializers import EnumFieldSerializerMixin
from dynamic_rest.fields import DynamicMethodField, DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer
# class
from hotelBooking.models.products import RoomPackage, RoomDayState, Product


class RoomDayStateSerializer(DynamicModelSerializer):

    class Meta:
        model = RoomDayState
        fields = ('s_point','s_price','d_point','d_price','date','state')


class ProductSerializer(DynamicModelSerializer):
    class Meta:
        model = Product

class RoomPackageSerializer(EnumFieldSerializerMixin , DynamicModelSerializer):

    roomstates = RoomDayStateSerializer(many=True,embed=True)

    class Meta(ProductSerializer.Meta):
        model = RoomPackage
        fields = ('id','breakfast','extra','default_s_point','default_s_price','default_d_point','default_d_price','created_on','roomstates',)



class RoomPackageCreateSerialzer(serializers.Serializer):
    hotel = serializers.IntegerField() #酒店
    room = serializers.IntegerField() #房型id
    price_type = serializers.IntegerField() # 单双同价?
    default_s_point = serializers.IntegerField() #
    default_s_price = serializers.IntegerField()
    default_d_point = serializers.IntegerField()
    default_d_price = serializers.IntegerField()
    breakfast = serializers.IntegerField() # 早餐类型
    bill = serializers.BooleanField()
    owner = serializers.IntegerField()

    customRoomName = serializers.CharField(allow_null=True,allow_blank=True)

    _inner_serialize = None
    class _inner_serializer(serializers.ModelSerializer):
        class Meta:
            model = RoomPackage

    def validate(self, attrs):
        room = attrs.get('room',-1)
        hotel = attrs.get('hotel')
        if(room == -1):
            from hotelBooking.models import Room
            room = Room(name=attrs.get('customRoomName'),hotel_id=hotel)
            room.save()
            attrs['room']= room.id
        del attrs['customRoomName']
        serializer = self._inner_serializer(data=attrs)
        serializer.is_valid(raise_exception=True)
        print('是合法的')
        print(serializer.validated_data)
        print('开始保存')
        # serializer.save()
        self._inner_serialize = serializer
        return {'succcess':True}

    def create(self, validated_data):
        instance = self._inner_serialize.save()
        return instance

    @property
    def data(self):
        return self._inner_serialize.data
