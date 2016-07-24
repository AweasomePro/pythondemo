from django.dispatch import Signal
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from hotelBooking.tasks import simple_notify
from hotelBooking.models.user import User
from hotelBooking.models.orders import HotelPackageOrder
from hotelBooking.module import push
from hotelBooking.models import User
from hotelBooking.serializers.orders import PartnerHotelPackageOrderSerializer

order_cancel = Signal(providing_args=["order", "cancelby"])

@receiver(order_cancel, )
def on_order_cancel(sender, order, cancelby, **kwargs):
    customer = order.customer
    seller = order.seller
    simple_notify.delay(seller.phone_number, message='你的订单已被取消')
    simple_notify.delay(customer.phone_number, message='你的订单已被取消')
    print('妈的怎么可以取消呢')


@receiver(post_save, sender=HotelPackageOrder,weak=False)
def on_order_create(sender, instance, signal, update_fields, using, created, **kwargs):
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
    print(sender)
    print(kwargs)
    if (created):# 新的订单被创建的情况
        pass
    print(update_fields)
    if('process_state' in update_fields):
        from hotelBooking.service.order.OrderService import HotelOrderProcessStateChangeHandler
        HotelOrderProcessStateChangeHandler(instance).handle()
    print(instance.tracker)
