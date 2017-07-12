# -*- coding: utf-8 -*-
import uuid
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from enumfields import Enum
from django.db import transaction
from jsonfield import JSONField
from model_utils.models import TimeStampedModel
from rest_framework.exceptions import APIException, PermissionDenied
from model_utils.managers import QueryManager, InheritanceManager

from chaolife.models.products import Product
from django.utils.timezone import datetime
from model_utils.fields import StatusField
from model_utils import Choices
from model_utils import FieldTracker
from model_utils.fields import MonitorField
from common.models import CreditCardMixin


class PaymentStatus(Enum):
    """
    支付状态
    """
    NOT_PAID = 0
    PARTIALLY_PAID = 1
    FULLY_PAID = 2
    CANCELED = 3
    DEFERRED = 4

    class Labels:
        NOT_PAID = _('not paid')
        PARTIALLY_PAID = _('partially paid')
        FULLY_PAID = _('fully paid')
        CANCELED = _('canceled')
        DEFERRED = _('deferred')


class ShippingStatus(Enum):
    # 资源还没有准备好
    NOT_SHIPPED = 0
    # 资源提供了，但是交易还没完成
    PARTIALLY_SHIPPED = 1
    # 交易完成订单处理完
    FULLY_SHIPPED = 2

    class Labels:
        NOT_SHIPPED = _('not shipped')
        PARTIALLY_SHIPPED = _('partially shipped')
        FULLY_SHIPPED = _('fully shipped')


class OrderStatusRole(Enum):
    NONE = 0
    INITIAL = 1
    COMPLETE = 2
    CANCELED = 3

    class Labels:
        NONE = _('none')
        INITIAL = _('initial')
        COMPLETE = _('complete')
        CANCELED = _('canceled')


class OrderQuerySet(models.QuerySet):
    def paid(self):
        return self.filter(payment_status=PaymentStatus.FULLY_PAID)

    def incomplete(self):
        return self.filter(status__role__in=(OrderStatusRole.NONE, OrderStatusRole.INITIAL))

    def complete(self):
        return self.filter(status__role=OrderStatusRole.COMPLETE)

    def valid(self):
        return self.exclude(status__role=OrderStatusRole.CANCELED)

    def recent_checkin(self):  # 今明入住
        from datetime import datetime
        return self.filter(checkin_time__in=())

    def since(self, days):
        return self.filter(
            order_date__gte=datetime.datetime.combine(
                datetime.date.today() - datetime.timedelta(days=days),
                datetime.time.min
            )
        )


@python_2_unicode_compatible
class Order(TimeStampedModel, models.Model):
    """
    当交易发生时 生成一个订单
    number
        一个用了表示订单的唯一键，customer可以用来查询
    订单是最重要的业务，应该将 收货人信息 配送信息 付款信息 结算信息 等分离成 辅表。。。
    """
    NOT_PAID = 0  # 未支付
    PARTIALLY_PAID = 1  # 部分支付
    FULLY_PAID = 2  # 完全支付
    CANCELED = 3  # 取消支付
    DEFERRED = 4  # 支付超时

    PAID_STATES = (
        (NOT_PAID, 'not paid'),
        (PARTIALLY_PAID, 'partially paid'),
        (FULLY_PAID, 'fully paid'),
        (CANCELED, 'canceled '),
        (DEFERRED, 'deferred'),
    )

    # 资源还没有准备好
    NOT_SHIPPED = 0
    # 资源提供了，但是交易还没完成
    PARTIALLY_SHIPPED = 1
    # 交易完成订单处理完
    FULLY_SHIPPED = 2
    # 虚拟物品无需发货
    NON_NEED_SHIPPED = 3

    SHIPPED_STATES = (
        (NOT_SHIPPED, '未发货'),
        (PARTIALLY_SHIPPED, '发货中'),
        (FULLY_SHIPPED, '已收货'),
        (NON_NEED_SHIPPED, '无需发货'),
    )

    INITIAL = 1
    PROCESSING = 2
    CANCELED = 3
    COMPLETE = 4
    REFUND = 5

    STATES_CHOICES = (
        (INITIAL, '订单发起'),
        (PROCESSING, '订单进行中'),
        (CANCELED, '订单取消'),
        (REFUND, '订单赔付完成'),
        (COMPLETE, '订单完成'),
    )

    number = models.CharField(primary_key=True, max_length=64, db_index=True, unique=True, blank=True, null=False,
                              verbose_name=_('订单号'))
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customer_orders', blank=True,
                                 on_delete=models.PROTECT, verbose_name=_('消费者'), )
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='seller_orders', blank=True, default=1000,
                               verbose_name=_('销售商'))
    product = models.ForeignKey(Product, related_name='product_orders', blank=True, null=True,
                                on_delete=models.SET_NULL,
                                verbose_name=_('产品'))
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders_modified', blank=True, null=True,
                                    on_delete=models.PROTECT, verbose_name=_('modifier user'), editable=False)
    deleted = models.BooleanField(db_index=True, default=False, verbose_name=_('删除'))
    # status = models.ForeignKey("OrderStatus", verbose_name=_('status'), on_delete=models.PROTECT)
    payment_status = models.IntegerField(choices=PAID_STATES, db_index=True, default=PARTIALLY_PAID,
                                         verbose_name=_('支付状态'))

    shipping_status = models.IntegerField(choices=SHIPPED_STATES, db_index=True, default=NOT_SHIPPED,
                                          verbose_name=_('运送状态'))
    status = models.IntegerField(choices=STATES_CHOICES, default=1, verbose_name=_('订单状态'))
    closed = models.BooleanField(default=False)  # 用于方便的判断该订单状态是否是用户可操作的状态
    success = models.BooleanField(default=False, help_text='订单完成')  # 也可以表示结算状态
    settled = models.BooleanField(default=False, verbose_name=_('已结算?'), help_text='是否已结算')
    amount = models.FloatField(verbose_name=_('订单总价(积分)'))
    objects = InheritanceManager()

    class Meta:
        app_label = 'chaolife'
        ordering = ("modified",)
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):  # pragma: no cover
        return self.customer.name + '的订单' + self.number


class OrderItem(models.Model):
    """
    An item for an order
    依赖于Order,所有有些信息就不需要申明了
    """
    order = models.ForeignKey(Order, related_name='items', verbose_name='Order', to_field='number',
                              on_delete=models.CASCADE)

    # 对于 酒店订房来说，跟所属Order 是一样的，考虑到未来 每个Order的item 可能不同，所以
    product_name = models.CharField(_('Product name'), max_length=255, null=True, blank=True,
                                    help_text=_("Product name at the moment of purchase"))
    product_code = models.CharField(_("Product default_code "), max_length=255, null=True, blank=True,
                                    help_text=_("Product default_code at the moment of purchase"))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Product"))

    objects = InheritanceManager()


from .fields import HourField


class HotelPackageOrder(Order):
    CUSTOMER_REQUIRE = 1
    CUSTOMER_CANCEL = 2
    CUSTOMER_BACK = 3
    SELLER_ACCEPT = 11
    SELLER_REFUSED = 12
    SELLER_BACK = 13
    SELLER_OPT_TIMEOUT = -100
    ARRIVE_CHECK_IN_TIME = 20
    OVER_CHECKOUT_TIME = 30
    PERFECT_SELL = 40
    REFUND_ORDER = -201
    REFUND_ORDER_PART_SUCCESS = -202
    REFUND_ORDER_SUCCESS = -200
    STATES = (
        (CUSTOMER_REQUIRE, '客户已经发起请求'),
        (CUSTOMER_CANCEL, '客户取消了入住'),  # 即代理商未接单 。不会扣除积分
        (CUSTOMER_BACK, '客户暂未入住，提前表示不能入住'),  # 即客户反悔，需扣除积分
        (SELLER_ACCEPT, '代理接收了订单,但是用户尚未入住'),
        (SELLER_REFUSED, '代理拒绝了订单'),  # 代理商直接拒绝了订单
        (SELLER_BACK, '代理提前表示某些原因导致不能入住了'),  # 即代理商 反悔。
        (SELLER_OPT_TIMEOUT, '代理超时确认，自动取消'),  # 系统自动帮助取消了订单
        (ARRIVE_CHECK_IN_TIME, '客户入住中(ing)'),  # 交易正常，并且时间到了用户的入住时间  （订单进行中）
        (OVER_CHECKOUT_TIME, '到达ckeckoutTime之后(表示等待结算)'),  # 到达checkout  之后，将订单标记为closed ,这个状态 没什么用。仅仅为了方便订单状态的检索
        (PERFECT_SELL, '交易积分已转到代理商账号'),  # 积分到达了代理商账号。
        (REFUND_ORDER, '退款赔付ing'),  # 正在进行退款赔付
        (REFUND_ORDER_PART_SUCCESS, '退款部分完成'),  # 正在进行退款赔付
        (REFUND_ORDER_SUCCESS, '退款完成')  # 正在进行退款赔付
    )

    DETAIL_STATES = (
        (CUSTOMER_REQUIRE, '客户已经发起请求'),
        (CUSTOMER_CANCEL, '客户取消了入住'),  # 即代理商未接单 。不会扣除积分
        (CUSTOMER_BACK, '客户暂未入住，提前表示不能入住'),  # 即客户反悔，需扣除积分
        (SELLER_ACCEPT, '代理接收了订单,但是用户尚未入住'),
        (SELLER_REFUSED, '代理拒绝了订单'),  # 代理商直接拒绝了订单
        (SELLER_BACK, '代理提前表示某些原因导致不能入住了'),  # 即代理商 反悔。
        (SELLER_OPT_TIMEOUT, '代理超时确认，自动取消'),  # 系统自动帮助取消了订单
        (ARRIVE_CHECK_IN_TIME, '客户入住中(ing)'),  # 交易正常，并且时间到了用户的入住时间  （订单进行中）
        (OVER_CHECKOUT_TIME, '到达ckeckoutTime之后'),  # 到达checkout  之后，将订单标记为closed ,这个状态 没什么用。仅仅为了方便订单状态的检索
        (PERFECT_SELL, '交易积分已转到代理商账号'),
        (REFUND_ORDER, '正在赔付中'),
        (REFUND_ORDER_PART_SUCCESS, '部分赔付完成'),
        (REFUND_ORDER_SUCCESS, '赔付成功')  # 积分到达了代理商账号。

    )
    # order = models.OneToOneField(Order,primary_key=True,to_field='number',on_delete=models.CASCADE)

    process_state = models.IntegerField(choices=STATES, default=CUSTOMER_REQUIRE, help_text='详细的订单进行的状态', db_index=True)
    process_state_change_at = MonitorField(monitor='process_state')

    # process_changed = MonitorField(monitor='process_state')
    tracker = FieldTracker()  # 跟踪数据的变化，如果数据没有 save 会返回None
    # 客户添加的额外信息
    checkin_time = models.DateField(verbose_name='入住时间', db_index=True)
    latest_checkin_hour = HourField(verbose_name='最晚到店时间')
    checkout_time = models.DateField(verbose_name='离店时间', db_index=True)
    total_front_prices = models.IntegerField(_('total need prices'), help_text='所需前台总价')
    # 币种
    price_type = models.IntegerField(default=1, help_text='单人价格|双人价格')
    total_need_points = models.IntegerField(_('total need points'), help_text='所需积分总和')
    breakfast = models.IntegerField(default=1, verbose_name='早餐类型', help_text=' 订单生成时,所记录的早餐类型')
    hotel_name = models.CharField(_('hotel name', ), max_length=255, help_text='hotel name at the moment of purchase')
    hotel_address = models.CharField(_('hotel address'), max_length=500, help_text='酒店地址')
    room_name = models.CharField(_('room name'), max_length=255, help_text='room name at the moment of purchase')
    request_remark = models.CharField(max_length=500, null=True, blank=True, help_text='用户订单要求')
    room_count = models.SmallIntegerField(verbose_name=_('房间件数'), default=1)
    people_count = models.SmallIntegerField(verbose_name=('入住人数'), default=1)
    comment = models.CharField(null=True, blank=True, help_text='消费评价', max_length=500)
    guests = JSONField(null=True, blank=True, help_text='入住人信息')
    reservation_number = models.CharField(max_length=20, verbose_name='预订号', help_text='酒店预订号',blank=True,)

    # 状态已经标记为完成的订单
    objects = QueryManager()
    closed_orders = QueryManager(closed=True)
    unaccept_orders = QueryManager(process_state=CUSTOMER_REQUIRE)
    # 需要保证离店时间大于当前时间
    accepted_orders = QueryManager(process_state=SELLER_ACCEPT)

    class Meta:
        app_label = 'chaolife'
        verbose_name = "酒店订单"
        verbose_name_plural = "酒店订单"
        permissions = (
            ("change_process_state", "能够操作改变订单过程状态"),
        )
        ordering = ('-process_state_change_at',)

    def __str__(self):

        return '{}-订单号{}:'.format(self.hotel_name, self.pk)

    # 在view中就应该进行了权限的判断

    def cancelBook(self, user):
        """
        取消预定
        :param user: 操作者 分为消费者 和加盟商
        :return:
        """
        if self.closed == True:
            raise PermissionDenied(detail='订单已关闭,无法进行该项操作')
        if (user == self.customer):
            # 计算 时间是否超期
            self.customer_cancel_order(user=user)
        elif (user == self.seller):
            self.partner_cancel_order(user)

    def customer_cancel_order(self, user):
        process_state = self.process_state
        if (process_state == self.CUSTOMER_REQUIRE):
            # 用户取消订单
            # todo 在有效时间内可以进行返回积分
            self.process_state = self.CUSTOMER_CANCEL
            self.closed = True
        elif (process_state == self.SELLER_ACCEPT):
            self.process_state = self.CUSTOMER_BACK
            self.closed = True
        else:
            raise APIException(detail='非法操作')
        self.save(update_fields=('process_state', 'closed'))
        return True, self
        # todo 对用户的积分不返回

    def refuse_by(self, user):
        if (self.process_state == self.CUSTOMER_REQUIRE):
            self.process_state = self.SELLER_REFUSED
            self.closed = True
            self.save()
            # 表示成功拒单，
            return True, 1
        else:
            return False, '当前状态无法进行此操作'

    def accept_by(self, user):
        if user == self.seller:
            if (self.process_state == self.CUSTOMER_REQUIRE):
                self.process_state = self.SELLER_ACCEPT
                self.save()
                # 表示成功拒单，
                return True, 1
            else:
                return False, '当前状态无法进行此操作'

    def tag_already_checkout(self):
        self.process_state = HotelPackageOrder.OVER_CHECKOUT_TIME
        self.closed = True
        self.success = True

    def tag_refund_partial_success(self):
        self.process_state = self.REFUND_ORDER_PART_SUCCESS
        self.save()

    def tag_refund_success(self):
        self.process_state = self.REFUND_ORDER_SUCCESS
        self.status = self.REFUND
        self.closed = True
        self.success = True
        self.save()

    def exist_process_state_in_history(self, process_state):
        # 检查是否有进行过该状态的改变，（默写状态的改变 在 siangal 中会触发一些列的操作，包括积分等等，要注意）
        return self.hotelorderoptlog_set.filter(process_state=process_state).exists()

    def tag_opt_tiemout(self):
        self.process_state = HotelPackageOrder.SELLER_OPT_TIMEOUT
        self.closed = True
        customer = self.customer
        # 创建记录
        self.save()
        with transaction.atomic():
            from account.models import User
            customer = User.objects.select_for_update().prefetch_related('customermember').get(id=customer.id)
            customer.customermember.points = customer.customermember.points + self.total_need_points
            customer.customermember.save()


class ClosedHotelOrderManger(models.Manager):
    def get_query_set(self):
        return super(ClosedHotelOrderManger, self).get_queryset().filter(closed=True)


class ClosedHotelPackageOrder(HotelPackageOrder):
    class Meta:
        proxy = True


class HotelPackageOrderItem(OrderItem):
    # 每天的积分和价格可能是不一样的，so do it
    day = models.DateField(_('check in day'), help_text='日期')
    point = models.IntegerField(_('need point'), help_text='所需积分(moment)')
    price = models.IntegerField(_('front price'), help_text='当天前台现付价格(moment)')

    class Meta:
        ordering = ('order', '-day',)


class HotelOrderCreditCardModel(CreditCardMixin):
    """行用卡凭证"""
    order = models.OneToOneField(HotelPackageOrder)

    class Meta:
        pass
