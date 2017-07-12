from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from message.tasks import simple_notify_user
from ..models import PointPay,InvoiceTimeLine
from account.models import User
from chaolife.tasks import notify_customer

@receiver(post_save,sender=PointPay)
def on_point_pay_success(sender,instance,created=False,**kwargs):
    pass