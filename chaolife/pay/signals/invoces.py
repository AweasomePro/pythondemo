from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from message.tasks import simple_notify_user
from ..models import Invoice,InvoiceTimeLine
from account.models import User
from chaolife.tasks import notify_customer

@receiver(post_save,sender=Invoice)
def invoice_save(sender,instance=None,created=False,**kwargs):
    print('instance')
    if instance and instance.tracker.has_changed('state') or created:
        InvoiceTimeLine.create_snapshot(instance)
        notify_customer.delay(instance.user.id,alert='发票申请成功')
    if instance.state == Invoice.STATE_REJECT and instance.tracker.has_changed('state') :
        user = User.objects.prefetch_related('customermember').select_for_update().get(phone_number = instance.user_id)
        user.customermember.invoiced_consumptions = F('invoiced_consumptions')-instance.value
        user.customermember.save()
        notify_customer.delay(instance.user.id,alert='发票进度更新了')
