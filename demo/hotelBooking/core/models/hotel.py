from django.db import models

from hotelBooking import User
from ..models.city import  City
from . import BaseModel
from .mixin import CheckMixin
# class RoomType(CheckMixin,models.Model):
#     name = models.CharField(max_length=255,null=False,blank=False,default='商务大床房')
#
#     class Meta:
#         app_label = 'hotelBooking'
#         verbose_name = "房型"
#         verbose_name_plural = "所有房型"
#
#     def __str__(self):
#         return self.name

class Hotel(models.Model):

    # 指定 主键 primary_key =True
    id = models.AutoField(primary_key=True)
    city = models.ForeignKey(City,verbose_name='所在城市',related_name='hotels')
    name = models.CharField(max_length=200,null=False,verbose_name='酒店名')
    address = models.CharField(max_length=255,null=False,verbose_name='地址')
    introduce = models.TextField(max_length=255,verbose_name='介绍')
    contact_phone = models.CharField(max_length=255,verbose_name='联系电话')
    agent = models.ManyToManyField(User)
    # types = models.ManyToManyField(RoomType)

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = "酒店"
        verbose_name_plural = "酒店"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name



class HouseManager(models.Manager):
    def get_queryset(self):
        return super(HouseManager, self).get_queryset().filter(checked=False,active=True)

class UncheckedHouseManager(models.Manager):
    def get_queryset(self):
        return super(UncheckedHouseManager,self).get_queryset().filter(checked=False)

class House(CheckMixin, BaseModel):
    """
    这个类表示发布的房源信息
    """
    id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(Hotel,verbose_name='所属酒店',related_name='hotel_houses')
    name = models.CharField(max_length=255,default='未定义房型名',blank=False,verbose_name='房型')

    objects = HouseManager()
    unchecked_objects = UncheckedHouseManager()

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = "房型"
        verbose_name_plural = "房型"

    def __unicode__(self):
        return self.name + ''

    def __str__(self):
        return self.name + ''

