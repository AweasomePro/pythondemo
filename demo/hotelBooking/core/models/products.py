from __future__ import unicode_literals, with_statement

from django.db import models
from . import BaseModel
from ..fields import InternalIdentifierField

import six
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from enumfields import Enum, EnumIntegerField
from hotelBooking.core.models.hotel import House

class ProductVisibility(Enum):
    VISIBLE_TO_ALL = 1
    VISIBLE_TO_LOGGED_IN = 2
    VISIBLE_TO_GROUPS = 3

    class Labels:
        VISIBLE_TO_ALL = _('visible to all')
        VISIBLE_TO_LOGGED_IN = _('visible to logged in')
        VISIBLE_TO_GROUPS = _('visible to groups')


class ShippingMode(Enum):
    NOT_SHIPPED = 0
    SHIPPED = 1

    class Labels:
        NOT_SHIPPED = _('not shipped')
        SHIPPED = _('shipped')

class ProductVerificationMode(Enum):
    NO_VERIFICATION_REQUIRED = 0
    ADMIN_VERIFICATION_REQUIRED = 1
    THIRD_PARTY_VERIFICATION_REQUIRED = 2

    class Labels:
        NO_VERIFICATION_REQUIRED = _('no verification required')
        ADMIN_VERIFICATION_REQUIRED = _('admin verification required')
        THIRD_PARTY_VERIFICATION_REQUIRED = _('third party verification required')

@python_2_unicode_compatible
class ProductType(BaseModel):
    identifier = InternalIdentifierField(unique=True)
    name = models.CharField(max_length=64, verbose_name=_('name'))

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = _('产品类型')
        verbose_name_plural = _('产品类型')


    def __str__(self):
        return self.name

class ProductQuerySet(QuerySet):
    pass

class Product(BaseModel):
    id = models.AutoField(primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('create on'))
    modified_on = models.DateTimeField(auto_now=True, editable=False, verbose_name=_('modified on'))
    deleted = models.BooleanField(default=False, editable=False, db_index=True, verbose_name=_('deleted'))
    type = models.ForeignKey(ProductType,verbose_name=_('product type'))
    #relation
    owner = models.ForeignKey('FranchiseeMember',)


    #Behavior
    # 这个产品是否需要 shipping(在这里，我表示需要代理商的人工处理验证)
    shipping_mode = EnumIntegerField(ShippingMode, default=ShippingMode.NOT_SHIPPED, verbose_name=_('shipping mode'))


    class Meta:
        app_label = 'hotelBooking'
        ordering = ('-id',)
        verbose_name = _('产品（数据库基类）')
        verbose_name_plural = _('产品（数据库基类）')

class HousePackage(BaseModel):
    HOUSE_STATE_CHOICES = (
        ('1', '充沛'),
        ('2', '满房')
    )
    product = models.OneToOneField(Product,)
    # detail product attribute
    house = models.ForeignKey(House, verbose_name='房型', related_name='housePackages')
    need_point = models.IntegerField(verbose_name='所需积分',default=0)
    front_price = models.IntegerField(verbose_name='前台现付价格')
    package_state = models.CharField(max_length=255, choices=HOUSE_STATE_CHOICES, default=HOUSE_STATE_CHOICES[0][1])
    detail = models.TextField()
    class Meta:
        app_label = 'hotelBooking'
        verbose_name = "套餐"
        verbose_name_plural = "套餐"





