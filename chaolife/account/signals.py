from django.core.signals import request_started
from django.conf import settings
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from authtoken.models import Token
from  account.models import PointRedemptionLog,PointRedemption,User,BillHistory,PartnerMember
from chaolife.tasks import notify_partner
from django.db import transaction

@receiver(request_started)
def request_start_callback(sender,**kwargs):
    print('Request start')


@receiver(post_save,sender= PointRedemption)
def pointRedemtion_save(sender,instance=None,created=False,**kwargs):
    print('发票来了 haha')
    PointRedemptionLog.create_snapshot(instance)
    notify_partner.delay(user_id=instance.user_id,alert='发票申请进度')
    pointRedemption = instance

    tracker = pointRedemption.tracker

    if tracker.has_changed('state'):
        if pointRedemption.state == PointRedemption.STATE_REJECT:
            #发票被拒绝了
            BillHistory.createForRedmptionReject(pointRedemption)