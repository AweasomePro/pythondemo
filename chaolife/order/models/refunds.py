from django.db import models
from django.utils.translation import ugettext_lazy as _
from ..helpers import get_next_refund_number
from chaolife.models.orders import Order,Product
from chaolifeProject.settings import AUTH_USER_MODEL
from common.models import TimeStampMixin
from djmoney.models.fields import MoneyField
from model_utils import FieldTracker

UNDEFINED_REASON ='请求补充退货原因'
class OrderRefund(models.Model):

    STATE_REQUIRE = 1
    STATE_ACCEPT = 2
    STATE_REJECT = -1
    STATE_REFUND_PARTIAL = 3
    STATE_SUCCESS = 100
    STATE_CHOICES =(
        (STATE_REQUIRE,'申请中'),
        (STATE_ACCEPT,'接收退货(款)'),
        (STATE_REFUND_PARTIAL,'赔付部分到账'),
        (STATE_REJECT,'拒绝退货(款)'),
        (STATE_SUCCESS,'退货完成'),
    )
    REFUND_REASON_CHOICES = (
        (1,'无法入住'),
        (0, '其他'),
    )

    STATE_DETAIL_CHOICES =(

    )
    code= models.CharField(primary_key=True,max_length=32,help_text='退款编号')
    order = models.ForeignKey(Order,verbose_name=_('订单'),)
    product = models.ForeignKey(Product,verbose_name=_('商品'))
    order_des = models.CharField(max_length=100,verbose_name=_('本次交易描述'))
    seller = models.ForeignKey(AUTH_USER_MODEL,verbose_name=_('商家'),related_name='sellerorders')
    proposer = models.ForeignKey(AUTH_USER_MODEL,verbose_name='申请人')
    proposer_refund_declaration  = models.CharField(max_length=200,verbose_name=_('用户退款说明'))
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    refund_reason = models.IntegerField(choices=REFUND_REASON_CHOICES,verbose_name=_('退货原因'))
    state = models.IntegerField(choices=STATE_CHOICES,verbose_name=_('申请状态'))
    detail_state = models.IntegerField(choices=STATE_DETAIL_CHOICES,verbose_name=_('详细状态'),blank=True,default=0)
    success_time = models.DateTimeField(verbose_name=_('退款成功时间'),blank=True,null=True)
    refund_points = models.FloatField(verbose_name=_('退还积分'))
    refunded = models.BooleanField(verbose_name=_('积分已赔付到账?'),help_text='这个状态不得重复更改,否则会造成积分多次赔付的情况',default=False)
    losses = models.BooleanField(verbose_name=_('有产生赔付'),default=False,)
    losses_money = models.FloatField(verbose_name=_('赔付现金金额'),default=0)
    tracker = FieldTracker()

    class Meta:
        verbose_name = "订单赔付"
        verbose_name_plural = "订单赔付"

    def __str__(self):
        return '订单'+self.order_id

    @classmethod
    def create(OrderRefund,hotelPackageOrder):
        orderRefund = OrderRefund(
            code= get_next_refund_number(),
            order=hotelPackageOrder,
            product=hotelPackageOrder.product,
            seller=hotelPackageOrder.seller,
            proposer=hotelPackageOrder.customer,
            refund_reason=1,
            state=1,
            refund_points=0,
        )
        orderRefund.save()