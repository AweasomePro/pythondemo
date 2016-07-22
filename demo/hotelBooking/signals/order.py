from django.dispatch import Signal
from django.dispatch import receiver
from hotelBooking.tasks import notify
from hotelBooking.models.user import User
order_cancel = Signal(providing_args=["order", "cancelby"])

@receiver(order_cancel,)
def order_process_change(sender, order, cancelby, **kwargs):
    customer = order.customer
    seller = order.seller
    notify.delay(seller.phone_number,message='你的订单已被取消')
    notify.delay(customer.phone_number,message='你的订单已被取消')

    print('妈的怎么可以取消呢')
