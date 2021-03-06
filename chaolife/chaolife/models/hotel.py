#-*- coding: utf-8 -*-
from django.db import models

from chaolife.models import User
from ..models.city import City
from .mixin import CheckMixin, ActiveMixin
from django.utils.translation import ugettext_lazy as _
from hotel.models import HotelType
class Hotel(ActiveMixin,models.Model):

    def check_unique(value):
        if Hotel.objects.filter(name=value).exists():
            raise
        pass

    TAG_CHOICES = (
        ('顶级奢华','顶级奢华'),
        ('特色设计','特色设计'),
        ('高级商务','高级商务'),
        ('经济体验','经济体验'),
        ('愉悦度假','愉悦度假'),
    )
    # 指定 主键 primary_key =True
    id = models.AutoField(primary_key=True,editable=False)
    city = models.ForeignKey(City,verbose_name='所在城市',related_name='hotels',on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200,null=False,verbose_name='酒店名',)
    type = models.ForeignKey(HotelType,blank=True,)
    english_name = models.CharField(max_length=255,null=True,verbose_name='英文名称',blank=True)
    smoking = models.BooleanField(default=True,verbose_name=_('can smoke '))
    brief_address = models.CharField(max_length=100,null=False,blank=True,verbose_name='简单的地址描述')
    established_des = models.CharField(max_length=50,null=False,blank=True,verbose_name='开业时间描述')
    address = models.CharField(max_length=255,null=False,verbose_name='地址')
    introduce = models.TextField(max_length=255,verbose_name='介绍')
    contact_phone = models.CharField(max_length=255,verbose_name='联系电话')
    cover_img = models.ImageField(verbose_name='封面图片')
    agent = models.ManyToManyField(User,blank=True)

    class Meta:
        app_label = 'chaolife'
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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Hotel,self).save(force_insert,force_update,using,update_fields)



class RoomManager(models.Manager):
    def get_queryset(self):
        return super(RoomManager, self).get_queryset()


class UncheckedRoomManager(models.Manager):
    def get_queryset(self):
        return super(UncheckedRoomManager, self).get_queryset().filter(checked=False)


class Room(CheckMixin, models.Model):
    """
    这个类表示发布的房源信息
    """
    id = models.AutoField(primary_key=True,editable=False)
    hotel = models.ForeignKey(Hotel,verbose_name='所属酒店',related_name='hotel_rooms')
    name = models.CharField(max_length=255,default='未定义房型名',blank=False,verbose_name='房型')

    objects = RoomManager()
    unchecked_objects = UncheckedRoomManager()

    class Meta:
        app_label = 'chaolife'
        verbose_name = "房型"
        verbose_name_plural = "房型"

    def __unicode__(self):
        return self.name + ''

    def __str__(self):
        return self.name + ''

    def save(self, *args,**kwargs):
        super(Room, self).save(*args, **kwargs)
