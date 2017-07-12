#-*- coding: utf-8 -*-
from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields import DynamicMethodField
from rest_framework import serializers

from chaolife.models.orders import HotelPackageOrder, Order,HotelPackageOrderItem,OrderItem
from chaolife.serializers.support import DynamicFieldsModelSerializer
from .card import HotelOrderCreditCardSerialzers


class OrderSerializer(DynamicModelSerializer):
    # number = serializers.IntegerField()
    # shipping_status = serializers.IntegerField

    class Meta:
        model = Order
        # fields = ('number','id')


class HotelOrderItemSerializer(DynamicModelSerializer):
    class Meta:
        model = HotelPackageOrderItem
        fields = ('point','price','day')


class HotelOrderSerializer(DynamicModelSerializer):
    guests = serializers.JSONField()
    order_items = DynamicMethodField(method_name='get_orderitems')

    def get_orderitems(self,hotelPackageOder):
        hotelPackageOrderItems = OrderItem.objects.filter(order=hotelPackageOder).select_subclasses(HotelPackageOrderItem)
        orderitems = HotelOrderItemSerializer(hotelPackageOrderItems,many=True,embed=True).data
        return orderitems

    class Meta:
        model = HotelPackageOrder
        name = 'order'
        plural_name = 'orders'

    def to_representation(self, instance):
        import json
        representation = super(HotelOrderSerializer, self).to_representation(instance)
        if representation.get('guests') == None:
            representation['guests'] = []
        if type(representation['guests']) == str:
            representation['guests'] = json.loads(representation['guests'])
        return representation

class HotelOrderDetailSerializer(HotelOrderSerializer):
    hotelordercreditcardmodel = HotelOrderCreditCardSerialzers()
    class Meta(HotelOrderSerializer.Meta):
        pass





