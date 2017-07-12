from django.db import models
from django.db.models import F
from model_utils.models import TimeStampedModel
from django.conf import settings
from chaolife.models import HotelPackageOrder
from model_utils.managers import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from account.models import User,PartnerMember,CustomerMember

class BillHistoryQuerySet(models.QuerySet):
    #warn 如果类型继续增加，应当在数据库层中再增加一个字段来表示
    def get_client_set(self):
        return self.filter(type__in=(1,2,5,6))
    def get_business_set(self):
        return self.filter(type__in=(3,4,6))


class BillHistory(TimeStampedModel):
    """
    用户积分记录
    """
    TYPE_RECHARGE_POINT = 1
    TYPE_BOOK_HOTEL = 2
    TYPE_SELL_ROOM = 3
    TYPE_POINT_REDEMPTION = 4
    TYPE_CANCEL_BOOK =5
    TYPE_SELL_REFUND =6
    ## 临时活动
    TYPE_INVITEE_USER = 301
    TYPE_FIRST_RECHARGE = 302

    des_invite_gains = '邀请用户活动奖励'

    TYPES = (
        (TYPE_RECHARGE_POINT,'积分充值'),
        (TYPE_BOOK_HOTEL,'酒店预订'),
        (TYPE_SELL_ROOM,'酒店资源销售'),
        (TYPE_SELL_REFUND,'酒店订单赔付'),
        (TYPE_POINT_REDEMPTION,'积分提现'),
        (TYPE_CANCEL_BOOK,'酒店预订取消,积分退还'),
        (TYPE_INVITEE_USER,'邀请用户,奖励积分'),
        (TYPE_FIRST_RECHARGE,'首充赠送'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='主体',)
    type = models.IntegerField(choices=TYPES)
    gains = models.IntegerField(help_text='获得或者扣除的积分',verbose_name=_('获得的积分'))
    business_id = models.CharField(max_length=64,null=False,help_text='对应的业务主键id')
    description = models.CharField(max_length=255,help_text='简短的业务描述，如（积分充值，酒店预订-北京-xx酒店）')

    objects = BillHistoryQuerySet.as_manager()

    class Meta:
        ordering = ('-modified',)


    @classmethod
    def createForFirstRechargeGift(cls,pointPay):
        with transaction.atomic():
            user = pointPay.user;
            gift_points = int(pointPay.number * 0.2);
            user.customermember.add_point(gift_points)
            cls(user=user, type=cls.TYPE_RECHARGE_POINT, gains=gift_points ,
                business_id=pointPay.number,
                description='首充赠送{} 积分'.format( gift_points)).save()

    @classmethod
    def createFromOrder(cls,order):
        if isinstance(order,HotelPackageOrder):
            #warn 丑陋 丑陋 丑陋 丑陋 丑陋 丑陋 丑陋 丑陋 丑陋 丑陋 丑陋 丑陋 丑陋 丑陋 丑陋 丑陋 丑陋 丑陋
            customer_instance = None
            seller_instance = None
            if (order.process_state == HotelPackageOrder.CUSTOMER_REQUIRE):
                customer_instance = cls(user=order.customer,
                               type= cls.TYPE_BOOK_HOTEL,
                               gains= -order.amount,
                               business_id=order.number,
                               description='酒店预订 - {}'.format(order.hotel_name)
                               )
            elif (order.process_state in
                      (HotelPackageOrder.CUSTOMER_CANCEL,
                       HotelPackageOrder.SELLER_REFUSED,
                       HotelPackageOrder.OVER_CHECKOUT_TIME,
                       HotelPackageOrder.SELLER_BACK
                       )
                  ):
                customer_instance = cls(user=order.customer,
                               type=cls.TYPE_CANCEL_BOOK,
                               gains= order.amount,
                               business_id=order.number,
                               description='{} 预订取消'.format(order.hotel_name)
                               )
            elif (order.process_state == HotelPackageOrder.SELLER_BACK):
                customer_instance = cls(user=order.customer,
                               type=cls.TYPE_CANCEL_BOOK,
                               gains= order.amount,
                               business_id=order.number,
                               description='{} 预订被取消'.format(order.hotel_name)
                               )
            elif (order.process_state == HotelPackageOrder.CUSTOMER_BACK):  # 用户  back 的情况下，可能会有积分到代理商账号
                if order.orderbill:
                    orderbill = order.orderbill
                    customer_instance = cls(user=order.customer,
                                            type=cls.TYPE_CANCEL_BOOK,
                                            gains=orderbill.refund_amount,
                                            business_id=order.number,
                                            description='{} 预订取消(部分返回)'.format(order.hotel_name)
                                            )
                    seller_instance = cls(user=order.seller,
                                          type=cls.TYPE_SELL_ROOM,
                                          gains=orderbill.seller_gains,
                                          business_id=order.number,
                                          description='酒店订单结算'.format(order.number)
                                          )

            elif(order.process_state == HotelPackageOrder.SELLER_OPT_TIMEOUT):
                customer_instance =cls(user=order.customer,
                               type=cls.TYPE_CANCEL_BOOK,
                               gains= order.amount,
                               business_id=order.number,
                               description='超时确认,退还积分 '.format(order.number)
                               )

            if not customer_instance is None: #不为空则保存
                customer_instance.save()
            if not seller_instance is None:
                seller_instance.save()

    @classmethod
    def createForRedmption(cls,pointRedemption):
        with transaction.atomic():
            partnerMember = PartnerMember.objects.select_for_update().get(user=pointRedemption.user)
            partnerMember.deduct_point(pointRedemption.points)
            partnerMember.invoice = F('invoice') - pointRedemption.points
            partnerMember.save(update_fields=('invoice',))
            instance = cls(user=pointRedemption.user,gains=-pointRedemption.points,type=cls.TYPE_POINT_REDEMPTION,description='积分提现申请')
            instance.save()

    @classmethod
    def createForRedmptionReject(cls,pointRedemption):
        with transaction.atomic():
            instance = cls(user=pointRedemption.user, gains=pointRedemption.points, type=cls.TYPE_POINT_REDEMPTION,
                           description='积分提现拒绝，积分退还')
            instance.save()
            partnerMember = PartnerMember.objects.select_for_update().get(user = pointRedemption.user_id)
            partnerMember.add_point(pointRedemption.points)
            #发票额度也要返还
            partnerMember.invoice +=pointRedemption.points
            print('返还了用户额度')
            partnerMember.save(update_fields=('invoice',))

    @classmethod
    def createForRefundOrderBill(cls, orderBill):
        seller_gains = orderBill.seller_gains
        with transaction.atomic():
            seller = orderBill.seller
            customer = orderBill.order.customer
            # warn 如果 seller 和customer 是同一个 会不会造成 死锁? => 不会，同一 transcation，死锁发生的情况类似于多线程锁死锁的情况
            seller = User.objects.select_for_update().get(id = seller.id)
            customer = User.objects.select_for_update().get(id = customer.id)
            if orderBill.refund_amount >0 and orderBill:
                customer.add_customer_points(orderBill.refund_amount)
                refund_order_bill = cls(
                    user=customer,
                    type=cls.TYPE_CANCEL_BOOK,
                    gains=orderBill.refund_amount,
                    business_id=orderBill.order.number,
                    description='获得订单赔付'
                )
                refund_order_bill.save()

            if orderBill.seller_gains!=0:
                seller.add_partner_points(orderBill.seller_gains)
                refund_order_bill = cls(
                    user=seller,
                    type=cls.TYPE_SELL_REFUND,
                    gains=orderBill.seller_gains,
                    business_id=orderBill.order,
                    description='卖家订单赔付'
                )
                refund_order_bill.save()
            orderBill.settled = True
            orderBill.save(update_fields=('settled',))

    @classmethod
    def createForInviter(cls, inviteRecord, pointPay, rewardPercent):
        with transaction.atomic():
            user = inviteRecord.inviter
            rewardPoint = int(pointPay.number * rewardPercent)

            if user.is_partner_member:
                # 如果是CHao 伙伴
                    partnerMember = PartnerMember.objects.select_for_update().get(user=user)
                    partnerMember.add_point(rewardPoint)
            elif User.is_customer_member:
                # 如果是普通顾客
                customerMember = CustomerMember.objects.select_for_update().get(user=user)
                customerMember.add_point(rewardPoint)
            inviteRecord.tag_is_rechargeed(pointPay,rewardPoint)
            #保存积分日志
            cls(user=user,type=cls.TYPE_RECHARGE_POINT,gains=pointPay.number*rewardPercent,business_id=pointPay.number,
                description='邀请用户{} 充值反馈积分{}'.format(pointPay.user.name,rewardPoint)).save()
