#-*- coding: utf-8 -*-
from django.db.models import Q,F,Count
from rest_framework import serializers
from rest_framework import fields
from datetime import datetime

from chaolife.exceptions import PointNotEnough
from account.models import User
from chaolife.core.order_creator.utils import generateHotelPackageProductOrder
from chaolife.exceptions import ConditionDenied
from chaolife.models import HotelOrderNumberGenerator
from chaolife.models import HotelPackageOrderItem,HotelOrderCreditCardModel
from chaolife.utils import dateutils
from common import appcodes
from common.utils.CreditCardUtil import isValidCard,NotSupportCardType
import re

from chaolife.models import HotelPackageOrder,Order


class HotelOrderCreateSerializer(serializers.ModelSerializer):

    # guests = serializers.JSONField(required=True,)
    price_type = serializers.IntegerField(write_only=True,)
    request_remark  = serializers.CharField(allow_null=True,allow_blank=True,)
    credit_card_type = serializers.CharField(allow_null=True,required=False)
    credit_card_number = serializers.CharField(allow_null=True,required=False)
    credit_card_validity_date = serializers.DateField(allow_null=True,required=False)

    class Meta:
        model = HotelPackageOrder
        name = 'order'

    latest_checkin_hour_pattern = re.compile(r'(\d{2}):00')

    def __init__(self,instance = None,data = None,context = None,**kwargs):
        request = context.get('request')
        user = request.user
        roomPackage = context.get('roomPackage')
        # request_data = data.copy()
        checkinTime = dateutils.formatStrToDate(data['checkinTime'])
        checkoutTime = dateutils.formatStrToDate(data['checkoutTime'])
        price_type = data['price_type']
        days = (checkoutTime - checkinTime).days
        daystates = roomPackage.roomstates.filter(date__gte=checkinTime, date__lt=checkoutTime)
        # 保证 state 为可预订状态
        if (daystates.count() != days):
            raise ConditionDenied(detail='该区间价格可能已被下架，不可用')
        if price_type == '1':
            sum_point = sum(daystate.s_point for daystate in daystates)
            sum_price = sum(daystate.s_price for daystate in daystates)
        else: #异价
            sum_point = sum(daystate.d_point for daystate in daystates)
            sum_price = sum(daystate.d_price for daystate in daystates)
        if user.customermember.points < sum_point:
            raise PointNotEnough()
        data['checkin_time'] = data['checkinTime']
        data['checkout_time'] = data['checkoutTime']
        data['hotel_address'] = roomPackage.hotel.address
        data['total_front_prices'] = sum_price
        data['amount'] =sum_point
        data['total_need_points'] = sum_point
        data['product'] =roomPackage.id
        data['room_name'] = roomPackage.room.name
        data['hotel_name'] = roomPackage.hotel.name
        data['breakfast'] = roomPackage.breakfast
        data['seller'] = roomPackage.owner_id
        data['customer'] = user.id
        data['payment_status'] = Order.FULLY_PAID
        data['state']=Order.INITIAL
        data['shipping_status']=Order.NON_NEED_SHIPPED
        super(HotelOrderCreateSerializer,self).__init__(instance=instance,data = data,context = context,**kwargs)
        self.request = request
        self.daystates = daystates
        self.roomPackage = roomPackage
        self.user = User.objects.select_for_update().get(id = request.user.id)
        self.is_support_card = False


    def validate_card(self,card_value,card_type):
        try:
            if not isValidCard(card_value,card_type):
                raise ConditionDenied('信用卡验证失败',code=appcodes.CODE_CREDIT_CARD_AUTHENTIC_ERROR)
        except NotSupportCardType:
            raise ConditionDenied('暂不支持的信用卡',code=appcodes.CODE_CREDIT_CARD_NOT_SUPPORT)

    class _man_infor(serializers.Serializer):
        name = serializers.CharField()
        phone_number = serializers.CharField()

    def validate_guests(self,value):
        import json
        serializer_ = self._man_infor(data=json.loads(value),many=True)
        serializer_.is_valid(raise_exception=True)
        print(value)
        return value


    def validate_checkinTime(self, value):
        if (value < datetime.today().date()):
            raise ConditionDenied(detail='checkinTime illegal', code=-100)
        self._validate_checkinTime= value
        return value


    def validate_checkoutTime(self, value):
        """
        Check that the blog post is about Django.
        """
        print('判断退出时间')
        if value <= self._validate_checkinTime:
            raise ConditionDenied(detail='checkouttime illegal', code=-100)
        return value

    def validate_latest_checkin_hour(self, value):
        # 直接判断比正则效率高
        match_res = self.latest_checkin_hour_pattern.match(value)
        if match_res:
            hour = int(match_res.groups()[0])
            if not (hour>=14 and hour <=24):
                raise ConditionDenied(detail='到店时间 illegal', code=-100)
        else:
            raise ConditionDenied(detail='到店时间 illegal', code=-100)
        if (hour > 18): # 大于18点，必须提供信用卡
                initial_data = self.initial_data
                print(initial_data)
                if not (initial_data.get('credit_card_number') and initial_data.get('credit_card_type')):
                    raise  ConditionDenied(detail='到店时间晚于18点必须提供信用卡', code=appcodes.CODE_CREDIT_CARD_NOT_PROVIDE)
                self.validate_card(self.initial_data['credit_card_number'],self.initial_data['credit_card_type'])
                self.is_support_card = True
        return value

    def validate(self, data):
        #
        exist = HotelPackageOrder.objects.\
            filter(customer=self.user, closed=False)\
            .exclude(Q(checkin_time__gte=data['checkout_time'])|Q(checkout_time__lte=data['checkin_time']))\
            .exists()
        if exist:
            #warn 上线需要限制
            # return data
            raise ConditionDenied(detail='存在该段时间内的未确认或入住订单,请先取消',code=appcodes.ORDER_HOTEL_EXIST_SAME_DAY_BUSINESS)
        if not (self.roomPackage.can_be_book(checkin_time=data['checkin_time'], checkout_time=data['checkout_time'])):
            raise ConditionDenied(detail='该价格已被下架', code=appcodes.CODE_THE_PRODUCT_IS_OFFLINE)
        return data

    def save(self, **kwargs):
        data = self.validated_data
        order_card = HotelOrderCreditCardModel()
        order_card.credit_card_number = data.pop('credit_card_number',None)
        order_card.credit_card_type = data.pop('credit_card_type',None)
        order_card.credit_card_validity_date = data.pop('credit_card_validity_date',None)
        self.validated_data['number'] = HotelOrderNumberGenerator.get_next_hotel_package_order_number(self.request)
        order = super(HotelOrderCreateSerializer,self).save(**kwargs)
        self.user.customermember.deduct_point(data['total_need_points'])
        orderItems = []
        for daystate in self.daystates:
            item = HotelPackageOrderItem(
                order=order,
                product_name='酒店预订',
                product_code=self.roomPackage.id,
                product=self.roomPackage,
                day=daystate.date,
                point=daystate.s_point,
                price=daystate.s_price,
            )
            item.save()
            orderItems.append(item)
        if self.is_support_card:
            order_card.order = order
            order_card.save()
        return order

    def to_representation(self, instance):
        import json
        representation = super(HotelOrderCreateSerializer, self).to_representation(instance)
        if representation.get('guests') == None:
            representation['guests'] = []
        if type(representation['guests']) == str:
            representation['guests'] = json.loads(representation['guests'])
        return representation






