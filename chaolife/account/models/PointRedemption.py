from django.db import models
from common.models import TimeStampMixin
from .user import User
from django.utils.translation import ugettext_lazy as _
from model_utils import FieldTracker

class PointRedemption(TimeStampMixin, models.Model):

    STATE_REJECT = -1
    STATE_REQUIRE = 1
    STATE_ACCEPT = 2
    STATE_SUCCESS = 3
    state_choices = (
        (STATE_REQUIRE,('申请提现'),),
        (STATE_ACCEPT,('提现请求申请成功'),),
        (STATE_SUCCESS,('提现成功'),),
        (STATE_REJECT,('请求拒绝'),)
    )
            
    state = models.IntegerField(choices=state_choices)
    user = models.ForeignKey(User,)
    points = models.PositiveIntegerField(verbose_name=_('提现积分'),null=False,blank=False,) # 相当于被冻结的积分
    card = models.CharField(max_length=40,verbose_name=_('提现卡号'),null=False,blank=False)
    bank = models.CharField(max_length=40,verbose_name=_('提现所属银行'),null=False,blank=False)
    tracker = FieldTracker()


    class Meta:
        ordering = ('-modified_at',)
        verbose_name ='提现申请'
        verbose_name_plural = '提现申请'

    def __str__(self):
        return self.user.name+'提现'+str(self.points)+'积分'

class PointRedemptionLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    point_redemption = models.ForeignKey(PointRedemption,on_delete=models.CASCADE)
    state = models.IntegerField(choices=PointRedemption.state_choices)
    class Meta:
        ordering = ('-created',)

    @classmethod
    def create_snapshot(cls,pointredemption):
        instance = cls(point_redemption=pointredemption,state=pointredemption.state)
        instance.save()