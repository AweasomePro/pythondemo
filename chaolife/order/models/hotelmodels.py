# -*- coding:utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import AutoCreatedField
from model_utils.models import TimeStampedModel
from account.models import PeopleInfor
from chaolife.models.orders import HotelPackageOrder
# Create your models here.


class HotelOrderOptLog(models.Model):
    hotelPackageOrder = models.ForeignKey(HotelPackageOrder,)
    created = AutoCreatedField(_('创建的时间'))
    process_state = models.IntegerField(help_text='操作后的状态',editable=False)
    description = models.CharField(max_length=254,help_text='对此次操作的描述')
    auto_opt = models.BooleanField(default=False,help_text='表示是否是系统自动的操作',editable=False)

    @staticmethod
    def create(hotelPackageOrder):
            hotelOrderOptLog = HotelOrderOptLog(hotelPackageOrder=hotelPackageOrder,process_state=hotelPackageOrder.process_state)
            hotelOrderOptLog.description = OrderOptLogTemplate.create_from_order(hotelPackageOrder)
            hotelOrderOptLog.save()

            print('optLog 保存了{}'.format(hotelOrderOptLog))
            return hotelOrderOptLog


class OrderOptLogTemplate():
    CUSTOMER_REQUIRE_TEMPLATE = '用户{customer},订购了{checkin_time}到{checkout_time} {hotel_name}-{room_name}{room_count}间,共计消费积分{total_need_points},另需前台现付{total_front_prices}'
    CUSTOMER_CANCEL = '用户取消了订单'
    CUSTOMER_BACKEND = '用户取消了订单-2'
    SELLER_ACCEPT = '代理商接受了订单'
    SELLER_REFUSED = '代理商拒绝了订单'
    SELLER_BACK = '代理商取消了订单'
    SELLER_OPT_TIMEOUT = '代理商超时未操作，系统自动取消了订单'
    ARRIVE_CHECK_IN_TIME = '到了用户 下单时提交的需要到店时间'
    OVER_CHECKOUT_TIME = '过了用户的离店时间'
    POINT_FLOW_TO_SELLER = '订单完成结算'
    REFUND_ORDER = '退款单'
    # CUSTOMER_CANCEL_AND_DEDUCT_POINT = '用户取消了订单，由于{reason},扣除了{point}积分'


    # (CUSTOMER_REQUIRE, '客户已经发起请求'),
    # (CUSTOMER_CANCEL, '客户取消了入住'),
    # (CUSTOMER_BACK, '客户暂未入住，提前表示不能入住'),
    # (SELLER_ACCEPT, '代理接收了订单,但是用户尚未入住'),
    # (SELLER_REFUSED, '代理拒绝了订单'),
    # (SELLER_BACK, '代理提前表示某些原因导致不能入住了'),
    # (SELLER_OPT_TIMEOUT, '代理超时确认，自动取消'),
    # (ARRIVE_CHECK_IN_TIME, '交易成功，时间到入住时间了(通常是在checkoutTime之后标记为此状态)'),
    # (OVER_CHECKOUT_TIME, '到达ckeckoutTime之后，将订单')

    @classmethod
    def create_from_order(cls, hotelPackageOrder):
        if (hotelPackageOrder.process_state ==  HotelPackageOrder.CUSTOMER_REQUIRE):
            return cls.CUSTOMER_REQUIRE_TEMPLATE.format(
                customer = hotelPackageOrder.customer,
                checkin_time = hotelPackageOrder.checkin_time,
                checkout_time = hotelPackageOrder.checkout_time,
                hotel_name = hotelPackageOrder.hotel_name,
                room_name = hotelPackageOrder.room_name,
                room_count = hotelPackageOrder.room_count,
                total_need_points = hotelPackageOrder.total_need_points,
                total_front_prices = hotelPackageOrder.total_front_prices,
            )
        elif (hotelPackageOrder.process_state == HotelPackageOrder.CUSTOMER_CANCEL):
            return cls.CUSTOMER_CANCEL
        elif (hotelPackageOrder.process_state == HotelPackageOrder.CUSTOMER_BACK):
            return cls.CUSTOMER_BACKEND
        elif (hotelPackageOrder.process_state == HotelPackageOrder.SELLER_ACCEPT):
            return cls.SELLER_ACCEPT.format()
        elif (hotelPackageOrder.process_state == HotelPackageOrder.SELLER_REFUSED):
            return cls.SELLER_REFUSED.format()
        elif (hotelPackageOrder.process_state == HotelPackageOrder.SELLER_BACK):
            return cls.SELLER_BACK
        elif (hotelPackageOrder.process_state == HotelPackageOrder.SELLER_OPT_TIMEOUT):
            return cls.SELLER_OPT_TIMEOUT
        elif (hotelPackageOrder.process_state == HotelPackageOrder.ARRIVE_CHECK_IN_TIME): #入住人信息
            return cls.ARRIVE_CHECK_IN_TIME
        elif (hotelPackageOrder.process_state == HotelPackageOrder.OVER_CHECKOUT_TIME):
            return cls.OVER_CHECKOUT_TIME
        elif (hotelPackageOrder.process_state == HotelPackageOrder.PERFECT_SELL):
            return cls.POINT_FLOW_TO_SELLER
        elif (hotelPackageOrder.process_state == HotelPackageOrder.REFUND_ORDER):
            return '订单退款'
        elif (hotelPackageOrder.process_state == HotelPackageOrder.REFUND_ORDER_PART_SUCCESS):
            return '订单部分退款成功'
        elif (hotelPackageOrder.process_state == HotelPackageOrder.REFUND_ORDER_SUCCESS):
            return '订单全部退款成功'







