
from django.db import models
from django.utils.translation import ugettext_lazy as _
from chaolife.models import Order
from model_utils.fields import MonitorField
from datetime import timedelta,datetime
from chaolifeProject.settings import AUTH_USER_MODEL
from .refunds import OrderRefund
from moneyed import Money
from account.models import BillHistory
class OrderBill(models.Model):

    SETTLEMENT_IMMEDIATELY = 1 # 立即结算
    SETTLEMENT_DELAY = 2# 延迟结算
    SETTLEMENT_CHOICE = (
        (SETTLEMENT_IMMEDIATELY,'立即结算'),
        (SETTLEMENT_DELAY,'延迟结算'),
    )

    order = models.OneToOneField(Order)
    seller = models.ForeignKey(AUTH_USER_MODEL,null=True)
    create_at = models.DateTimeField(auto_now_add=True,verbose_name=_('订单创建时间'))
    commission = models.FloatField(verbose_name=_('佣金(积分)'),default=0)
    order_amount = models.FloatField(verbose_name=_('订单总额'))
    refund_amount = models.FloatField(verbose_name=_('退单金额'),help_text='退单金额，可能是用户取消订单，退还的金额')
    capital_settlement = models.IntegerField( choices=SETTLEMENT_CHOICE,verbose_name=_('商家结算方式'),help_text='资金结算方式，有包括立即结算，和延时结算')
    delay_settlement_time = models.DateTimeField(verbose_name=_('需要结算的日期'),null=True)
    seller_gains = models.FloatField(verbose_name=_('卖家收益积分'),help_text='在产生积分赔付的情况下，该值可能为负')
    settled  = models.BooleanField(default=False,verbose_name=_('已结算?'),help_text='是否已结算')
    settled_at = MonitorField(monitor='settled',when=[True,])

    class Meta:
        verbose_name = "订单结算"
        verbose_name_plural = "订单结算"

    def __str__(self):
        return '订单'+self.order_id

    @classmethod
    def create_for_roomOrder_cancel(cls,roomOrder,refund_amount,):
        order_amount = roomOrder.amount
        assert refund_amount < order_amount
        can_gains_points = order_amount - refund_amount
        sell_gains = can_gains_points * 0.75
        commission = can_gains_points * 0.25
        orderbill = cls(
            order=roomOrder,
            seller=roomOrder.seller,
            commission=commission,
            order_amount=order_amount,
            refund_amount=refund_amount,
            capital_settlement=cls.SETTLEMENT_IMMEDIATELY,
            delay_settlement_time = datetime.now(),
            seller_gains=sell_gains,
            settled=True
        )
        if orderbill.capital_settlement == cls.SETTLEMENT_IMMEDIATELY:
            customer = roomOrder.customer
            seller = roomOrder.seller
            seller.add_partner_points(can_gains_points)
            customer.add_customer_points(refund_amount)
        return orderbill

    @classmethod
    def create_for_perfect_room_sell(cls,hotelPackageOrder):
        orderbill = cls(
            order=hotelPackageOrder,
            seller=hotelPackageOrder.seller,
            commission=hotelPackageOrder.amount * 0.25,
            order_amount=hotelPackageOrder.amount,
            refund_amount=0,
            capital_settlement=cls.SETTLEMENT_DELAY,
            seller_gains=hotelPackageOrder.amount * 0.75,
            delay_settlement_time=hotelPackageOrder.checkout_time + timedelta(days=2),
            settled=False
        )
        return orderbill

    @classmethod
    def create_for_refund_order(cls,orderRefund):
        order = orderRefund.order
        seller_gains = -orderRefund.losses_money * 10
        orderBill = cls(
            order=order,
            seller=order.seller,
            order_amount=order.amount,
            refund_amount=orderRefund.refund_points,
            capital_settlement=cls.SETTLEMENT_IMMEDIATELY,
            commission=0,
            seller_gains =  seller_gains,
            settled = False
        )
        orderBill.save()
        BillHistory.createForRefundOrderBill(orderBill)

