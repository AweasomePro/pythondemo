#-*- coding: utf-8 -*-
from  rest_framework import serializers
from chaolife.models import HotelOrderCreditCardModel

class HotelOrderCreditCardSerialzers(serializers.ModelSerializer):
    class Meta:
        model = HotelOrderCreditCardModel
        exclude = ('id','order',)