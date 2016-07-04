from hotelBooking.core.models.orders import HotelPackageOrder, Order,HotelPackageOrderSnapShot
from hotelBooking.core.serializers.support import DynamicFieldsModelSerializer
from rest_framework import serializers
from rest_framework import models

class HotelPackgeOrderSnapShotSerialier(DynamicFieldsModelSerializer):
    # hotel_name = serializers.CharField()

    class Meta:
        model = HotelPackageOrderSnapShot
        exclude=('id','hotel_package_order')
        # fields =('hotel_name','house_name',)


class OrderSerializer(DynamicFieldsModelSerializer):
    # number = serializers.IntegerField()
    shipping_status = serializers.IntegerField

    class Meta:
        model = Order
        # fields = ('number','id')



class CustomerOrderSerializer(serializers.Serializer):
    order = OrderSerializer()
    hotelpackageordersnapshot = HotelPackgeOrderSnapShotSerialier()
    class Meta:
        model = HotelPackageOrder
        exclude = ('id','uuid','franchisee','customer')
