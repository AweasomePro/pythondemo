#-*- coding: utf-8 -*-
from __future__ import unicode_literals, with_statement

import uuid

from model_utils.models import TimeStampedModel

from chaolife.models.mixin import CheckMixin
from model_utils.managers import InheritanceManager
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from enumfields import Enum
from chaolife.models.city import City
from chaolife.models.hotel import Room, Hotel
from chaolifeProject import settings
from jsonfield.fields import JSONField
from chaolife.exceptions import ConditionDenied
from common import appcodes
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

class ProductQuerySet(QuerySet):
    pass


class Product(CheckMixin,TimeStampedModel, models.Model):
    Product_Types = (
        (1,'酒店订房'),
    )
    # 产品的唯一标识
    # id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    type = models.IntegerField(choices=Product_Types, default= Product_Types[0][0],verbose_name=_('product type'),editable=False)
    #relation
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,)

    #Behavior
    # 这个产品是否需要 shipping(在这里，我表示需要代理商的人工处理验证)
    # shipping_mode = EnumIntegerField(enum=ShippingMode, default=ShippingMode.NOT_SHIPPED, verbose_name=_('shipping mode'))

    objects = InheritanceManager()

    class Meta:
        app_label = 'chaolife'
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


class CanBookingRoomPackageManager(models.Manager):
    def get_query_set(self):
        return RoomPackageQuerySet(self.model, using=self._db).filter(active=True,deleted=False,checked = True)


class RoomPackage(Product):
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

    PRICE_SAME = 1
    PRICE_DIFF = 2
    Price_Types = (
        (PRICE_SAME, '单双同价'),
        (PRICE_DIFF, '单双异价'),
    )
    city = models.ForeignKey(City,verbose_name='城市',help_text='所属城市')
    hotel = models.ForeignKey(Hotel,verbose_name='酒店')
    # hotel_name = models
    room = models.ForeignKey(Room, verbose_name='房型', related_name='roomPackages')
    hotel_name = models.CharField(max_length=254,verbose_name='酒店名')
    room_name = models.CharField(max_length=254,verbose_name='房型名')
    breakfast = models.IntegerField(choices=Breakfast_Types,default=Breakfast_Types[0][0],verbose_name='早餐类型')
    bill = models.BooleanField(default=True,verbose_name=_('提供发票'))
    smoking = models.BooleanField(default=True,verbose_name='有烟?',help_text=_('0 表示 无烟房,1表示没有明确表示'))
    # 作为默认的积分
    price_type = models.IntegerField(choices=Price_Types,default=Price_Types[0][0],verbose_name='价格类型')
    default_s_point = models.PositiveIntegerField(verbose_name='默认单人所需积分', default=0)
    # price that guest need pay at hotel front desk
    # 作为默认的价格
    default_s_price = models.PositiveIntegerField(verbose_name='默认单人现付价格')
    default_d_point = models.PositiveIntegerField(verbose_name='默认双人所需积分', default=0)
    # price that guest need pay at hotel front desk
    # 作为默认的价格
    default_d_price = models.PositiveIntegerField(verbose_name='默认双人现付价格')

    extra = JSONField(verbose_name=_("Extra fields"),
                      help_text=_("Arbitrary information for this roompackage object."),null=True,blank=True)
    # the hotel package is open to guests?
    # detail = models.TextField(default="",blank=True)
    objects = RoomPackageManager()
    canBookingProduct = CanBookingRoomPackageManager()

    class Meta:
        app_label = 'chaolife'
        verbose_name = "套餐"
        verbose_name_plural = "套餐"



    @property
    def _validate_state_be_book(self):
        return self.active and not self.deleted and self.checked

    def can_be_book(self, checkin_time, checkout_time):
        exists_full_day = self.roompackage.roomstates.filter(date__gte=checkin_time.strftime('%Y-%m-%d'), date__lt=checkout_time.strftime('%Y-%m-%d'), state=0).exists()
        return (not exists_full_day) and self._validate_state_be_book




class RoomDayState(TimeStampedModel):
    ROOM_STATE_EMPTY = 0
    ROOM_STATE_ENOUGH = 1
    ROOM_STATE_FEW = 2

    ROOM_STATES = (
        (ROOM_STATE_ENOUGH,'尚还有房'),
        (ROOM_STATE_EMPTY,'没有房了')
    )
    agent = models.ForeignKey(settings.AUTH_USER_MODEL)
    hotel = models.ForeignKey(Hotel,related_name='roomstates')
    city = models.ForeignKey(City,related_name='roomstates',on_delete=models.CASCADE)
    roomPackage = models.ForeignKey(RoomPackage, related_name='roomstates',on_delete=models.CASCADE)
    s_point = models.PositiveIntegerField(verbose_name='当天单人所需积分', default=0)
    s_price = models.PositiveIntegerField(verbose_name='当天单人前台现付价格')
    d_point = models.PositiveIntegerField(verbose_name='当天双人所需积分', default=0)
    d_price = models.PositiveIntegerField(verbose_name='当天双人前台现付价格',)
    room = models.ForeignKey(Room)
    date = models.DateField()
    state = models.IntegerField(choices=ROOM_STATES,default=ROOM_STATE_ENOUGH)

    class Meta:
        app_label = 'chaolife'
        verbose_name = "房间类型状态"
        verbose_name_plural = "房间类型状态"
        ordering = ('agent','date')
        get_latest_by = 'date'

    def __str__(self):
        return str(self.date)+'-'+ '有房' if self.state==self.ROOM_STATE_ENOUGH else '满'