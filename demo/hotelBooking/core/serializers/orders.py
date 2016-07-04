from hotelBooking.core.models.orders import HotelPackageOrder, Order,HotelPackageOrderSnapShot
from hotelBooking.core.serializers.support import DynamicFieldsModelSerializer
from rest_framework import serializers
from rest_framework import models
class HotelPackgeOrderSnapShotSerialier(serializers.Serializer):
    class Meta:
        model = HotelPackageOrderSnapShot

class OrderSerializer(DynamicFieldsModelSerializer):
    # number = serializers.IntegerField()
    shipping_status = serializers.IntegerField

    class Meta:
        model = Order
        # fields = ('number','id')



class CustomerOrderSerializer(serializers.Serializer):
    order = OrderSerializer()
    snapshot = HotelPackgeOrderSnapShotSerialier()
    class Meta:
        model = HotelPackageOrder
