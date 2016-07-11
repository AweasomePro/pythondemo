from __future__ import unicode_literals, with_statement

from drf_enum_field.fields import EnumField

from hotelBooking import City
from hotelBookingProject import settings
from . import BaseModel

import six
import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from enumfields import Enum, EnumIntegerField
from hotelBooking.core.models.hotel import House, Hotel
from model_utils import Choices
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

    # class Labels:
    #     NO_VERIFICATION_REQUIRED = _('no verification required')
    #     ADMIN_VERIFICATION_REQUIRED = _('admin verification required')
    #     THIRD_PARTY_VERIFICATION_REQUIRED = _('third party verification required')

class ProductTypeEnum(Enum):
    HOTEL_HOUSE_PACKAGE = 'hotel_house_package'

    class Labels:
        HOTEL_HOUSE_PACKAGE = _('hotel house package')

from model_utils.managers import InheritanceManager
class ProductQuerySet(QuerySet):
    pass

class Product(BaseModel):
    Product_Types = (
        (1,'酒店订房'),
    )
    # 产品的唯一标识
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_on = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('create on'))
    modified_on = models.DateTimeField(auto_now=True, editable=False, verbose_name=_('modified on'))
    deleted = models.BooleanField(default=False, editable=False, db_index=True, verbose_name=_('deleted'))
    type = models.IntegerField(choices=Product_Types, default= Product_Types[0][0],verbose_name=_('product type'))
    #relation
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    #Behavior
    # 这个产品是否需要 shipping(在这里，我表示需要代理商的人工处理验证)
    # shipping_mode = EnumIntegerField(enum=ShippingMode, default=ShippingMode.NOT_SHIPPED, verbose_name=_('shipping mode'))

    objects = InheritanceManager()

    class Meta:
        app_label = 'hotelBooking'
        ordering = ('-id',)
        verbose_name = _('产品（数据库基类）')
        verbose_name_plural = _('产品（数据库基类）')

    def __str__(self):
        return '{0}的酒店房间资源'.format(self.owner.user.name)


class HousePackageQuerySet(models.query.QuerySet):
    pass

class HousePackageManager(models.Manager):
    def get_query_set(self):
        return HousePackageQuerySet(self.model,using=self._db)



class HousePackage(Product):
    # HOUSE_STATE_CHOICES = (
    #     ('1', '充沛'),
    #     ('2', '满房')
    # )
    # detail product attribute
    house = models.ForeignKey(House, verbose_name='房型', related_name='housePackages')
    # agent = models.ForeignKey(settings.AUTH_USER_MODEL)
    need_point = models.IntegerField(verbose_name='所需积分',default=0)
    front_price = models.IntegerField(verbose_name='前台现付价格')
    detail = models.TextField()

    objects = HousePackageManager()

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = "套餐"
        verbose_name_plural = "套餐"

    def __str__(self):
        return '{}-{}-{}-{}'.format(self.house.hotel.city.name,self.house.hotel.name,self.house.name,self.id)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        print('调用一次')
        super(HousePackage,self).save(force_insert=force_insert,force_update=force_update,using=using,
                                      update_fields=update_fields)

    def can_be_book(self,checkinTime,checkoutTime):
        exists_full_day = self.housepackage_roomstates.filter(date__gte=checkinTime,date__lte=checkoutTime,state=0).exists()
        return (not exists_full_day) and self.deleted == False


class AgentRoomTypeState(models.Model):

    ROOM_STATE_ENOUGH = 1
    ROOM_STATE_FEW = 2
    ROOM_STATE_NO_EMPTY = 3

    ROOM_STATES = (
        (ROOM_STATE_ENOUGH,'room is enough'),
        (ROOM_STATE_FEW,'room is few'),
        (ROOM_STATE_NO_EMPTY,'room has no empty')
    )
    agent = models.ForeignKey(settings.AUTH_USER_MODEL)
    hotel = models.ForeignKey(Hotel,related_name='hotel_roomstates')
    city = models.ForeignKey(City,related_name='city_roomstates')
    housePackage = models.ForeignKey(HousePackage,related_name='housepackage_roomstates')
    house_type = models.ForeignKey(House)
    date = models.DateField()
    state = models.IntegerField(choices=ROOM_STATES,default=ROOM_STATE_ENOUGH)

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = "房间类型状态"
        verbose_name_plural = "房间类型状态"
