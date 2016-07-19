from __future__ import unicode_literals, with_statement

import uuid

from hotelBooking.models.mixin import CheckMixin

from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from enumfields import Enum
from hotelBooking.models.city import City
from hotelBooking.models.hotel import Room, Hotel
from hotelBookingProject import settings
from jsonfield.fields import JSONField
from . import BaseModel


class ShippingMode(Enum):
    NOT_SHIPPED = 0
    SHIPPED = 1

    class Labels:
        NOT_SHIPPED = _('not shipped')
        SHIPPED = _('shipped')

class ProductTypeEnum(Enum):
    HOTEL_ROOM_PACKAGE = 'hotel_room_package'

    class Labels:
        HOTEL_ROOM_PACKAGE = _('hotel room package')

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
    type = models.IntegerField(choices=Product_Types, default= Product_Types[0][0],verbose_name=_('product type'),editable=False)
    #relation
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,)

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
        return '{0}的酒店房间资源'.format(self.owner.name)


class RoomPackageQuerySet(models.query.QuerySet):
    pass

class RoomPackageManager(models.Manager):
    def get_query_set(self):
        return RoomPackageQuerySet(self.model, using=self._db)

class RoomPackage(CheckMixin, Product):
    # ROOM_STATE_CHOICES = (
    #     ('1', '充沛'),
    #     ('2', '满房')
    # )
    # detail product attribute
    Breakfast_Types = (
        (1, '无早'),
        (2, '单早'),
        (3, '双早'),
    )
    hotel = models.ForeignKey(Hotel,verbose_name='酒店')
    room = models.ForeignKey(Room, verbose_name='房型', related_name='roomPackages')
    breakfast = models.IntegerField(choices=Breakfast_Types,default=Breakfast_Types[0][0],verbose_name='早餐类型')
    # agent = models.ForeignKey(settings.AUTH_USER_MODEL)
    # 作为默认的积分
    default_point = models.IntegerField(verbose_name='默认所需积分', default=0)
    # price that guest need pay at hotel front desk
    # 作为默认的价格
    default_front_price = models.IntegerField(verbose_name='默认前台现付价格')
    extra = JSONField(verbose_name=_("Extra fields"),
                      help_text=_("Arbitrary information for this roompackage object."),null=True,blank=True)
    # the hotel package is open to guests?
    # detail = models.TextField(default="",blank=True)
    objects = RoomPackageManager()

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = "套餐"
        verbose_name_plural = "套餐"

    # def __str__(self):
    #     return '{}-{}-{}'.format(self.room.hotel.city.name,self.room.hotel.name,self.room.name)

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     print('调用一次')
    #
    #     super(RoomPackage,self).save(force_insert=force_insert,force_update=force_update,using=using,
    #                                   update_fields=update_fields)



    def can_be_book(self,checkinTime,checkoutTime):
        exists_full_day = self.roompackage_daystates.filter(date__gte=checkinTime,date__lte=checkoutTime,state=0).exists()
        return (not exists_full_day) and self.deleted == False

class RoomDayState(models.Model):
    ROOM_STATE_ENOUGH = 1
    ROOM_STATE_FEW = 2
    ROOM_STATE_NO_EMPTY = 3

    ROOM_STATES = (
        (ROOM_STATE_ENOUGH,'room is enough'),
        (ROOM_STATE_FEW,'room is few'),
        (ROOM_STATE_NO_EMPTY,'room has no empty')
    )
    agent = models.ForeignKey(settings.AUTH_USER_MODEL)
    hotel = models.ForeignKey(Hotel,related_name='roomstates')
    city = models.ForeignKey(City,related_name='roomstates')
    roomPackage = models.ForeignKey(RoomPackage, related_name='roomstates')
    need_point = models.IntegerField(verbose_name='当天所需积分',default=0)
    # price that guest need pay at hotel front desk
    # 作为默认的价格
    front_price = models.IntegerField(verbose_name='当天前台现付价格')
    room = models.ForeignKey(Room)
    date = models.DateField()
    state = models.IntegerField(choices=ROOM_STATES,default=ROOM_STATE_ENOUGH)

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = "房间类型状态"
        verbose_name_plural = "房间类型状态"
        get_latest_by = 'date'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # if self.default_point == 0:
        #     self.default_point = self.roomPackage.default_point
        # todo  设置一个默认值，注意 不要访问外数据库
        super(self,RoomDayState).save(force_insert=False, force_update=False, using=None,
             update_fields=None)