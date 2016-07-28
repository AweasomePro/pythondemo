from django.db import models

from hotelBooking.models import User
from ..models.city import  City
from . import BaseModel
from .mixin import CheckMixin, ActiveMixin
from django.utils.translation import ugettext_lazy as _
# class Room(CheckMixin,models.Model):
#     name = models.CharField(max_length=255,null=False,blank=False,default='商务大床房')
#
#     class Meta:
#         app_label = 'hotelBooking'
#         verbose_name = "房型"
#         verbose_name_plural = "所有房型"
#
#     def __str__(self):
#         return self.name

class Hotel(ActiveMixin,models.Model):

    # 指定 主键 primary_key =True
    id = models.AutoField(primary_key=True,editable=False)
    city = models.ForeignKey(City,verbose_name='所在城市',related_name='hotels')
    name = models.CharField(max_length=200,null=False,verbose_name='酒店名')
    smoking = models.BooleanField(default=False,verbose_name=_('can smoke '))
    address = models.CharField(max_length=255,null=False,verbose_name='地址')
    introduce = models.TextField(max_length=255,verbose_name='介绍')
    contact_phone = models.CharField(max_length=255,verbose_name='联系电话')
    cover_img = models.ImageField(verbose_name='封面图片')
    agent = models.ManyToManyField(User,blank=True)
    # types = models.ManyToManyField(Room)

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = "酒店"
        verbose_name_plural = "酒店"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def min_price(self):
        #todo 求得该酒店最低的价格，并做cache缓存，该字段用于前端的界面展示
        #warn  !! 该方法会联合多表查询，要做很多的性能优化
        pass

class RoomManager(models.Manager):
    def get_queryset(self):
        return super(RoomManager, self).get_queryset()

class UncheckedRoomManager(models.Manager):
    def get_queryset(self):
        return super(UncheckedRoomManager, self).get_queryset().filter(checked=False)

class Room(CheckMixin, BaseModel):
    """
    这个类表示发布的房源信息
    """
    id = models.AutoField(primary_key=True,editable=False)
    hotel = models.ForeignKey(Hotel,verbose_name='所属酒店',related_name='hotel_rooms')
    name = models.CharField(max_length=255,default='未定义房型名',blank=False,verbose_name='房型')

    objects = RoomManager()
    unchecked_objects = UncheckedRoomManager()

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = "房型"
        verbose_name_plural = "房型"

    def __unicode__(self):
        return self.name + ''

    def __str__(self):
        return self.name + ''

    def save(self, *args,**kwargs):
        print(args)
        print(kwargs)
        super(Room, self).save(*args, **kwargs)
