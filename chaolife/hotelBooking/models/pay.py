import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from hotelBooking.models import User
from hotelBooking.models.mixin import DateStateMixin


class Pay(DateStateMixin,models.Model):
    PAY_METHODS = (
        (1,_('支付宝')),
    )
    PAY_STATUS = (
        (1,_('未支付')),
        (2,_('支付成功')),
    )
    trade_no = models.CharField(editable=False,db_index=True,max_length=32)
    unit_price = models.PositiveIntegerField(_('单位价格(元)'),default=1)
    number = models.PositiveIntegerField(_('购买的数量'))
    total_price = models.FloatField(_('总价'))
    user = models.ForeignKey(User)
    status = models.IntegerField(choices=PAY_STATUS,default=PAY_STATUS[0][0])
    pay_method = models.IntegerField(choices=PAY_METHODS,default=PAY_METHODS[0][0])
    class Meta:
        app_label = 'hotelBooking'
