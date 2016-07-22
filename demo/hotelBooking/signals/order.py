from django.dispatch import Signal
from django.dispatch import receiver

order_cancel = Signal(providing_args=["order", "cancelby"])

@receiver(order_cancel,)
def order_canceld(sender,**kwargs):
    print('妈的怎么可以取消呢')
