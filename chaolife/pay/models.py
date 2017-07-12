# -*- coding:utf-8 -*-
import uuid

from django.db import models
from django.db import transaction

from chaolifeProject import settings
from django.utils.translation import ugettext_lazy as _
from chaolife.models import User
from chaolife.models.mixin import DateStateMixin
from common.fiels import PositiveFloatField
from common.models import TimeStampMixin
from model_utils import FieldTracker
from message.tasks import simple_notify_user


class PointPay(DateStateMixin, models.Model):
    """
    积分充值
    """
    PAY_METHOD_ZFB =1
    PAY_METHOD_WX =2
    PAY_METHODS = (
        (PAY_METHOD_ZFB,_('支付宝')),
        (PAY_METHOD_WX,_('微信'))
    )

    PAY_UN_CHECKED =0
    PAY_CHECKED = 1

    PAY_STATUS = (
        (PAY_UN_CHECKED,_('未支付')),
        (PAY_CHECKED,_('支付成功')),
    )
    trade_no = models.CharField(editable=False,db_index=True,max_length=32)
    unit_price = models.PositiveIntegerField(_('单位价格(元)'),default=1)
    number = models.PositiveIntegerField(_('购买的数量'))
    total_price = models.FloatField(_('总价'),help_text=_('交易总价'))
    user = models.ForeignKey(User,to_field=( 'id'))
    status = models.IntegerField(choices=PAY_STATUS,default=PAY_STATUS[0][0],help_text=_('表示是否支付成功，需要第三方服务回调才能确认'))
    pay_method = models.IntegerField(choices=PAY_METHODS,default=PAY_METHODS[0][0],help_text=_('支付渠道'))

    class Meta:
        app_label = 'pay'


    def is_first_recharge(self,):
        if PointPay.objects.filter(user=self.user,status=self.PAY_CHECKED).count() == 1:
            return True
        else:
            return False

    @staticmethod
    def handle_pay_succcess(out_trade_no):
        with transaction.atomic():
            pay = PointPay.objects.prefetch_related('user', ).select_for_update().get(trade_no=out_trade_no)
            if (pay.status == PointPay.PAY_UN_CHECKED):  # 只对这个处理
                customermember = pay.user.customermember
                pay.status = PointPay.PAY_CHECKED
                customermember.points = customermember.points + pay.number
                customermember.consumptions += pay.total_price
                customermember.save(update_fields=('points', 'consumptions'))
                from account.models import BillHistory
                bill = BillHistory(
                    user=pay.user,
                    type=BillHistory.TYPE_RECHARGE_POINT,
                    gains=pay.number,
                    business_id=pay.trade_no,
                    description='积分充值'.format()
                )
                pay.save()
                bill.save()
                # 积分充值活动的处理
                from account.invitation.service import promotion_service
                promotion_service(pay)
                simple_notify_user.delay(pay.user.id, alert='您充值的积分{number}已到账'.format(number=pay.number))

# class InvoiceQuerySet(models.QuerySet):
#     handleing_state = (Invoice.STATE_REQUIRE,Invoice.STATE_ACCEPT,Invoice.SENDING)
#
#     def inHandle(self):
#         return self.filter(state__in=InvoiceQuerySet.handleing_state)


class Invoice(TimeStampMixin,models.Model):
    STATE_REJECT = -1
    STATE_REQUIRE = 1
    STATE_ACCEPT = 2
    STATE_SENDING = 3
    STATE_COMPLETE = 4

    state_choices = (
        (STATE_REQUIRE, ('申请发票'),),
        (STATE_ACCEPT, ('发票请求申请成功'),),
        (STATE_REJECT, ('发票请求拒绝'),),
        (STATE_SENDING, ('发票邮寄成功'),),
        # (STATE_COMPLETE,('发票完成'),)
    )
    content_type_choices = (
        (1,('代订房费')),
        (2,('旅游服务费')),
        (3,('服务费')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,to_field='phone_number')
    value = PositiveFloatField(verbose_name=_('开票金额'))
    state = models.IntegerField(choices=state_choices)
    title = models.CharField(max_length=255,verbose_name=_('发票抬头'),help_text='发票抬头')
    type = models.IntegerField(choices=content_type_choices)
    email = models.EmailField(verbose_name=_('邮寄地址'))
    reject_reason = models.CharField(max_length=50,help_text='拒绝原因',verbose_name=_('拒绝原因'),null=False,blank=True)
    viewed = models.BooleanField(default=False,verbose_name=_('该发票已关闭'))
    tracker = FieldTracker(fields=('state','viewed'))

    class Meta:
        ordering = ('-modified_at','-id')
        verbose_name = '用户发票'
        verbose_name_plural = '用户发票'

    def __str__(self):
        return '{}-金额:{}'.format(self.user,self.value)



class InvoiceTimeLine(DateStateMixin,models.Model):
    invoice = models.ForeignKey(Invoice)
    state = models.IntegerField(choices=Invoice.state_choices)

    @classmethod
    def create_snapshot(cls,invoice):
        instance = cls(state=invoice.state,invoice=invoice)
        instance.save()