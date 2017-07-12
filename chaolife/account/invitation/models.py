from django.db import models
from django.db.models import Count, Sum
from django.db.models import F
from django.db import transaction
from common.models import CreateMixin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from ..models import PartnerMember,CustomerMember,User
from ..models import BillHistory
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'account.models.User')


class ActivationManager(models.Manager):
    pass


class InviteRecord(CreateMixin, models.Model):
    inviter = models.ForeignKey(AUTH_USER_MODEL,)
    invitee = models.OneToOneField(AUTH_USER_MODEL,related_name='inviteeRecord')
    recharged = models.BooleanField(default=False,verbose_name='已充值',help_text='被邀请者是否已充值')
    recharge_point_amount = models.IntegerField(verbose_name=_('被邀请者充值数量'),default=0)
    inviter_reward_points = models.IntegerField(verbose_name=_('邀请用户奖励积分'),default=0)
    recharge_time = models.DateTimeField(blank=True,help_text='首次充值的时间',null=True,)

    class Meta:
        pass
    def tag_is_rechargeed(self,pointPay,reward_points):
        self.recharged = True
        self.recharge_point_amount = pointPay.number
        self.inviter_reward_points = reward_points
        self.recharge_time = pointPay.create_at
        self.save()

    @classmethod
    def get_invited_nums(InviteRecord,inviter):
        return InviteRecord.objects.filter(inviter=inviter,recharged=True).count()

    @classmethod
    def handle_new_invitee_recharge(InviteRecord, inviteRecord, pointPay):
        now_invited_and_recharged_numb = InviteRecord.get_invited_nums(inviteRecord.inviter)
        rewardPercent = InviteRecord.getRewardPercent(now_invited_and_recharged_numb)
        BillHistory.createForInviter(inviteRecord, pointPay, rewardPercent)

    @staticmethod
    def getRewardPercent(number):
        """
        根据人数，得到当前能够获得的返现百分比
        :return:
        """
        if number<=10:
            return 0.05
        elif number<=20:
            return 0.07
        elif number<=50:
            return 0.1
        elif number>50:
            return 0.15
        return 0



    @classmethod
    def get_invited_reward_points(InviteRecord,inviter):
        return InviteRecord.objects.filter(inviter=inviter,recharged=True).aggregate(allreward_pints = Sum(F('inviter_reward_points')))
