from dynamic_rest.serializers import DynamicEphemeralSerializer, DynamicModelSerializer
from hotelBooking.core.models.orders import HotelPackageOrder, Order,HotelPackageOrderSnapShot
from hotelBooking.core.serializers.support import DynamicFieldsModelSerializer
from rest_framework import serializers
from rest_framework import models
from rest_framework.utils.serializer_helpers import ReturnDict
class HotelPackgeOrderSnapShotSerialier(DynamicFieldsModelSerializer):
    # hotel_name = serializers.CharField()

    class Meta:
        model = HotelPackageOrderSnapShot
        exclude=('id','hotel_package_order')
        # fields =('hotel_name','house_name',)


class OrderSerializer(DynamicFieldsModelSerializer):
    # number = serializers.IntegerField()
    # shipping_status = serializers.IntegerField

    class Meta:
        model = Order
        # fields = ('number','id')



class CustomerOrderSerializer(DynamicModelSerializer):
    # order = OrderSerializer()
    hotelpackageordersnapshot = HotelPackgeOrderSnapShotSerialier()

    class Meta:
        model = HotelPackageOrder
        name = 'order'
        # exclude = ('id','order')

    def to_representation(self, instance):
        print('to_presentation')
        orderDict = super(CustomerOrderSerializer,self).to_representation(instance)
        return orderDict


