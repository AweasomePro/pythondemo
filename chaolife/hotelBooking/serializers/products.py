import datetime
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from drf_enum_field.serializers import EnumFieldSerializerMixin
from dynamic_rest.fields import DynamicMethodField, DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer
# class
from hotelBooking.models.products import RoomPackage, RoomDayState, Product
from hotelBooking.tasks import createRoomDaysetsFormRoomPackage

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

class RoomPackageCreateSerializer(serializers.ModelSerializer):
    customRoomName = serializers.CharField(write_only=True)

    class Meta(ProductSerializer.Meta):
        model = RoomPackage
        read_only_fields =('checked','active')


    def create(self,validate_data):
        room = validate_data.get('room')
        name = validate_data.get('customRoomName')
        hotel = validate_data.get('hotel')
        if (room == -1):
            from hotelBooking.models import Room
            room = Room(name=name, hotel_id=hotel)
            room.save()
            validate_data['room'] = room.id
        print('是合法的')
        del validate_data['customRoomName']
        obj = super(RoomPackageCreateSerializer,self).create(validate_data)
        return obj

