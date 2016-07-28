from django.dispatch import Signal
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from hotelBooking.tasks import simple_notify
from hotelBooking.models.user import User
from hotelBooking.models.orders import HotelPackageOrder
from hotelBooking.module import push
from hotelBooking.models import User
from hotelBooking.serializers.orders import PartnerHotelPackageOrderSerializer
from hotelBooking.serializers.orders import CustomerOrderSerializer
order_cancel = Signal(providing_args=["order", "cancelby"])

@receiver(order_cancel, )
def on_order_cancel(sender, order, cancelby, **kwargs):
    customer = order.customer
    seller = order.seller
    simple_notify.delay(seller.phone_number, message={
        'alert': '订单操作',
        'order':CustomerOrderSerializer(order).data,
        'action':'com.pushHotel.action',
    })
    simple_notify.delay(customer.phone_number, message={
        'alert':'订单操作',
        'order':PartnerHotelPackageOrderSerializer(order).data,
        'action':'com.BusinessHotel.action'}
                        )
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
    from hotelBooking.service.order.OrderService import HotelOrderProcessStateChangeHandler
    if (created):# 新的订单被创建的情况
        HotelOrderProcessStateChangeHandler(instance).handle()
    print(update_fields)
    if(update_fields and 'process_state' in update_fields):
        HotelOrderProcessStateChangeHandler(instance).handle()
    print(instance.tracker)
