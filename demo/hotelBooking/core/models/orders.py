import uuid

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.conf import settings
from django.db import models
from django.db.transaction import atomic
from django.utils.crypto import get_random_string
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from enumfields import Enum, EnumIntegerField
from django.db.models.query import QuerySet
from . import BaseModel

# from parler.managers import TranslatableQuerySet
# from parler.models import TranslatableModel, TranslatedFields
import datetime

from hotelBooking.core.fields import (InternalIdentifierField,)

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


class OrderStatusQuerySet(QuerySet):
    def _default_for_role(self, role):
        """
        Get the default order status for the given role.

        :param role: The role to look for.
        :type role: OrderStatusRole
        :return: The OrderStatus
        :rtype: OrderStatus
        """
        try:
            return self.get(default=True, role=role)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("No default %s OrderStatus exists." % getattr(role, "label", role))

    def get_default_initial(self):
        return self._default_for_role(OrderStatusRole.INITIAL)

    def get_default_canceled(self):
        return self._default_for_role(OrderStatusRole.CANCELED)

    def get_default_complete(self):
        return self._default_for_role(OrderStatusRole.COMPLETE)

@python_2_unicode_compatible
class OrderStatus(BaseModel):
    identifier = InternalIdentifierField(db_index=True,blank=False,unique=True)
    ordering = models.IntegerField(db_index=True,default=0,verbose_name=_('ordering'))
    # order 的状态
    role = EnumIntegerField(OrderStatusRole,db_index=True, default=OrderStatusRole.NONE, verbose_name=_('role'))
    # i dont know
    default = models.BooleanField(default=False,db_index=True,verbose_name=_('default'))

    objects = OrderStatusQuerySet.as_manager()

    name = models.CharField(verbose_name=_('name'), max_length=64)

    class Meta:
        app_label = 'hotelBooking'

    def __str__(self):
        return self.safe_translation_getter("name",default=self.identifier)

    def save(self, *args, **kwargs):
        super(OrderStatus,self).save(*args,**kwargs)
        if self.default and self.role != OrderStatusRole.NONE:
            # If this status is the default ,make the other for this role non-default
            OrderStatus.objects.filter(role=self.role).exclude(pk = self.pk).update(default = False)

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

    created_on = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('created on'))
    modified_on = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('modified on'))
    identifier = InternalIdentifierField(unique=True, db_index=True, verbose_name=_('order identifier'))
    # TODO: label is actually a choice field, need to check migrations/choice deconstruction
    label = models.CharField(max_length=32, db_index=True, verbose_name=_('label'))
    # The key shouldn't be possible to deduce (i.e. it should be random), but it is
    # not a secret. (It could, however, be used as key material for an actual secret.)
    key = models.CharField(max_length=32, unique=True, blank=False, verbose_name=_('key'))

    number = models.CharField(max_length=30, db_index=True, unique=True, blank=True, null=True,)

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    reference_number = models.CharField(
        max_length=64, db_index=True, unique=True, blank=True, null=True,
        verbose_name=_('reference number'))

    # Contact information
    customer = models.ForeignKey("CustomerMember",related_name='customer_orders',blank=True,null=True,
                                  on_delete=models.PROTECT,verbose_name=_('customer'))
    product = models.ForeignKey("Product",related_name='product_orders',blank=True,null=True,
                                on_delete=models.PROTECT,
                                verbose_name=_('product'))

    # Status
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders_modified', blank=True, null=True,
                                    on_delete=models.PROTECT, verbose_name=_('modifier user'))
    deleted = models.BooleanField(db_index=True, default=False, verbose_name=_('deleted'))
    status = models.ForeignKey("OrderStatus", verbose_name=_('status'), on_delete=models.PROTECT)
    payment_status = EnumIntegerField(PaymentStatus, db_index=True, default=PaymentStatus.NOT_PAID,
                                      verbose_name=_('payment status'))
    shipping_status = EnumIntegerField(ShippingStatus, db_index=True, default=ShippingStatus.NOT_SHIPPED,
                                       verbose_name=_('shipping status'))

    objects = OrderQuerySet.as_manager()

    class Meta:
        app_label = 'hotelBooking'
        ordering = ("created_on",)
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):  # pragma: no cover
        return "去重载这个方法吧"

class HotelPackgeOrderSnapShot(models.Model):
    pass

class HotelPackageOrder(Order):
    order = models.OneToOneField(Order)
    snapshot = models.ForeignKey(HotelPackgeOrderSnapShot,blank=True)

