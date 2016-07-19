import uuid

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from jsonfield.fields import JSONField
from enumfields import Enum
from django.db import transaction
from rest_framework.exceptions import APIException, PermissionDenied

# from parler.managers import TranslatableQuerySet
# from parler.models import TranslatableModel, TranslatedFields
from hotelBooking.models.products import Product
from django.utils.timezone import datetime
# def get_unique_id_str():
#     return str(uuid.uuid4())

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

# class OrderStatusQuerySet(QuerySet):
#     def _default_for_role(self, role):
#         """
#         Get the default order status for the given role.
#
#         :param role: The role to look for.
#         :type role: OrderStatusRole
#         :return: The OrderStatus
#         :rtype: OrderStatus
#         """
#         try:
#             return self.get(default=True, role=role)
#         except ObjectDoesNotExist:
#             raise ObjectDoesNotExist("No default %s OrderStatus exists." % getattr(role, "label", role))
#
#     def get_default_initial(self):
#         return self._default_for_role(OrderStatusRole.INITIAL)
#
#     def get_default_canceled(self):
#         return self._default_for_role(OrderStatusRole.CANCELED)
#
#     def get_default_complete(self):
#         return self._default_for_role(OrderStatusRole.COMPLETE)

# @python_2_unicode_compatible
# class OrderStatus(BaseModel):
#     identifier = InternalIdentifierField(db_index=True,blank=False,unique=True)
#     ordering = models.IntegerField(db_index=True,default=0,verbose_name=_('ordering'))
#     # order 的状态
#     role = EnumIntegerField(OrderStatusRole,db_index=True, default=OrderStatusRole.NONE, verbose_name=_('role'))
#     # i dont know
#     default = models.BooleanField(default=False,db_index=True,verbose_name=_('default'))
#
#     objects = OrderStatusQuerySet.as_manager()
#
#     name = models.CharField(verbose_name=_('name'), max_length=64)
#
#     class Meta:
#         app_label = 'hotelBooking'
#
#     def __str__(self):
#         return self.safe_translation_getter("name",default=self.identifier)
#
#     def save(self, *args, **kwargs):
#         super(OrderStatus,self).save(*args,**kwargs)
#         if self.default and self.role != OrderStatusRole.NONE:
#             # If this status is the default ,make the other for this role non-default
#             OrderStatus.objects.filter(role=self.role).exclude(pk = self.pk).update(default = False)
#
class OrderQuerySet(models.QuerySet):
    def paid(self):
        return self.filter(payment_status=PaymentStatus.FULLY_PAID)

    def incomplete(self):
        return self.filter(status__role__in=(OrderStatusRole.NONE, OrderStatusRole.INITIAL))

    def complete(self):
        return self.filter(status__role=OrderStatusRole.COMPLETE)

    def valid(self):
        return self.exclude(status__role=OrderStatusRole.CANCELED)

    def since(self, days):
        return self.filter(
            order_date__gte=datetime.datetime.combine(
                datetime.date.today() - datetime.timedelta(days=days),
                datetime.time.min
            )
        )

@python_2_unicode_compatible
class Order(models.Model):
    """
    当交易发生时 生成一个订单
    number
        一个用了表示订单的唯一键，customer可以用来查询

    """
    NOT_PAID = 0
    PARTIALLY_PAID = 1
    FULLY_PAID = 2
    CANCELED = 3
    DEFERRED = 4
    PAID_STATES = (
        (NOT_PAID,'not paid'),
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

    SHIPPED_STATES = (
        (NOT_SHIPPED, 'not shipped'),
        (PARTIALLY_SHIPPED, 'not shipped'),
        (FULLY_SHIPPED, 'fully shipped'),
    )
    id = models.AutoField(primary_key=True,auto_created=True)
    # uuid = models.UUIDField(max_length=50, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=30, db_index=True, unique=True, blank=True,null=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='customer_orders', blank=True,
                                 on_delete=models.PROTECT, verbose_name=_('customer'))
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='seller_orders',blank=True)
    product = models.ForeignKey(Product, related_name='product_orders', blank=True,
                                on_delete=models.PROTECT,
                                verbose_name=_('product'))
    created_on = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('created on'))
    modified_on = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('modified on'))

    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders_modified', blank=True, null=True,
                                    on_delete=models.PROTECT, verbose_name=_('modifier user'))
    deleted = models.BooleanField(db_index=True, default=False, verbose_name=_('deleted'))
    # status = models.ForeignKey("OrderStatus", verbose_name=_('status'), on_delete=models.PROTECT)
    payment_status = models.IntegerField(choices = PAID_STATES,db_index=True, default=PARTIALLY_PAID,
                                      verbose_name=_('payment status'))

    shipping_status = models.IntegerField(choices=SHIPPED_STATES,db_index=True, default=NOT_SHIPPED,
                                       verbose_name=_('shipping status'))

    objects = OrderQuerySet.as_manager()

    class Meta:
        app_label = 'hotelBooking'
        ordering = ("created_on",)
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):  # pragma: no cover
        return self.customer.name+'的订单'+self.number

class OrderItem(models.Model):
    """
    An item for an order
    依赖于Order,所有有些信息就不需要申明了
    """
    order = models.ForeignKey(Order,related_name='items',verbose_name='Order')

    # 对于 酒店订房来说，跟所属Order 是一样的，考虑到未来 每个Order的item 可能不同，所以
    product_name = models.CharField(_('Product name'),max_length=255,null=True,blank=True,
        help_text=_("Product name at the moment of purchase"))
    product_code = models.CharField(_("Product code "),max_length=255,null=True,blank=True,
        help_text=_("Product code at the moment of purchase"))
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True,verbose_name=_("Product"))

class HotelPackageOrder(Order):
    CUSTOMER_REQUIRE = 0x01
    CUSTOMER_CANCEL = 0x02
    CUSTOMER_BACKEND = 0x03
    FRANCHISES_ACCEPT = 0x10
    FRANCHISES_REFUSED = 0x20
    FRANCHISES_BACKED = 0x30
    STATES = (
        (CUSTOMER_REQUIRE, '客户已经发起请求'),
        (CUSTOMER_CANCEL, '客户取消了入住'),
        (CUSTOMER_BACKEND, '客户暂未入住，提前表示不能入住'),
        (FRANCHISES_ACCEPT, '代理接收了订单'),
        (FRANCHISES_REFUSED, '代理拒绝了订单'),
        (FRANCHISES_BACKED, '代理提前表示某些原因导致不能入住了'),
    )
    # order = models.OneToOneField(Order)

    checkin_time = models.DateField(verbose_name='入住时间')
    checkout_time = models.DateField(verbose_name='离店时间')
    closed = models.BooleanField(default=False)
    process_state = models.IntegerField(choices=STATES,default=CUSTOMER_REQUIRE,help_text='订单进行的状态')
    # 客户添加的额外信息
    total_front_prices = models.IntegerField(_('total need prices'),help_text='所需前台总价')
    total_need_points = models.IntegerField(_('total need points'),help_text='所需积分总和')

    hotel_name = models.CharField(_('hotel name',),max_length=255,help_text='hotel name at the moment of purchase')
    room_name = models.CharField(_('room name'),max_length=255,help_text='room name at the moment of purchase')

    request_notes = models.TextField(null=True, blank=True,help_text='用户订单要求')

    comment = models.TextField(null=True,blank=True,help_text='消费评价')
    guests = JSONField(null=True,blank=True,help_text='入住人信息')

    class Meta:
        app_label = 'hotelBooking'
        permissions = (
            ("change_process_state","能够操作改变订单过程状态"),
        )

    def cancelBook(self,user):
        if(user != self.customer and user!= self.seller):
            raise PermissionDenied(detail='你无权进行此操作')
        """
        取消预定
        :param user: 操作者 分为消费者 和加盟商
        :return:
        """
        if self.closed == True:
            raise PermissionDenied(detail='订单已关闭,无法进行该项操作')
        if(user == self.customer):
            # 计算 时间是否超期
            self.customer_cancel_order(user=user)
        elif(user == self.seller):
            self.partner_cancel_order(user)

    def customer_cancel_order(self,user):
        process_state = self.process_state
        if (process_state == self.CUSTOMER_REQUIRE):
                # 用户取消订单
                # todo 在有效时间内可以进行返回积分
                self.process_state = self.CUSTOMER_CANCEL
                self.closed = True
        elif( hex(process_state)[-1] == self.FRANCHISES_ACCEPT):
            self.process_state = self.CUSTOMER_BACKEND
            self.closed = True
        else:
            raise APIException(detail='非法操作')
        self.save(update_fields=('process_state','closed'))
            #todo 对用户的积分不返回

    def partner_cancel_order(self,user):
        process_state = self.process_state
        if (process_state == self.FRANCHISES_ACCEPT):
            self.process_state = self.FRANCHISES_BACKED
            self.closed = True

    def refused_order(self,user):
        if user == self.seller:
            self.process_state = self.FRANCHISES_REFUSED
            self.closed = True
            pass
        else:
            raise  PermissionDenied(detail='你无权进行此操作，因为你不是该订单的所有者')

class HotelPackageOrderItem(OrderItem):
    day = models.DateField(_('check in day'),help_text='日期')
    point = models.IntegerField(_('need point'),help_text='所需积分(moment)')
    front_price = models.IntegerField(_('front price'),help_text='当天前台现付价格(moment)')

# class HotelPackageOrderSnapShot(models.Model):
#     hotel_id = models.IntegerField()
#     room_type_id = models.IntegerField()
#     hotel_name = models.CharField(max_length=255)
#     room_type_name = models.CharField(max_length=255)
#     default_front_price = models.IntegerField()
#     default_point = models.IntegerField()
#     hotel_package_order = models.OneToOneField(HotelPackageOrder)
#     # def create_from_source(self,house_package):
#     #     room = house_package.room
#     #     hotel = house_package.room.hotel
#     #     self.hotel_id = hotel.id
#     #     self.room_type_id = room.id
#     #     self.default_point = house_package.default_point
#     #     self.default_front_price = house_package.default_front_price
#     #     self.hotel_name = hotel.name
#     #     self.room_type_name = room.name
#     class Meta:
#         app_label = 'hotelBooking'

