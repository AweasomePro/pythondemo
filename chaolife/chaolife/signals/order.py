#-*- coding: utf-8 -*-
from django.dispatch import Signal
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from chaolife.tasks import notify_user
from account.models import User
from chaolife.models.orders import HotelPackageOrder
from chaolife.serializers.orders import HotelOrderSerializer
from order.models import HotelOrderOptLog
from ..service.order.OrderService import refund_hotel_order, push_notify_client
from sms.tasks import notify_customer_order_crate_success

order_cancel = Signal(providing_args=["order", "cancelby"])


@receiver(post_save, sender=HotelPackageOrder,weak=False)
def on_order_create(instance, signal, update_fields, using, created, **kwargs):
    """
    当有新的订单被创建时，处理
    :param sender:
    :param instance:
    :param signal:
    :param update_fields:
    :param using:
    :param created:
    :param kwargs:
    :return:
    """
    from chaolife.service.order.OrderService import HotelOrderProcessStateChangeHandler
    from account.models import BillHistory
    # if (created):# 新的订单被创建的情况
    #     HotelOrderProcessStateChangeHandler(instance).handle() #目前的通知都是统一的,所以
    tracker = instance.tracker
    if created:
        push_notify_client(instance)
        notify_customer_order_crate_success.delay(instance.customer.phone_number,instance.customer.name,str(instance.checkin_time),str(instance.checkout_time),instance.hotel_name)
    if tracker.has_changed('process_state'):
        if instance.process_state == HotelPackageOrder.REFUND_ORDER:
            #创建退款单
            refund_hotel_order(instance)
        if not created:# warn 同样也是短信通知，不过不知道为什么 在create new instance 的情况下，celery任务有时候会报 数据库找不到该订单的错误，需要了解这个回调的时候数据库中该 条记录到底是创建成功了没有
            HotelOrderProcessStateChangeHandler(instance).handle()
    BillHistory.createFromOrder(instance)
    HotelOrderOptLog.create(instance)
