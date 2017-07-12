#-*- coding: utf-8 -*-
from django.db import models

from common.models import TimeStampMixin
from ..models.hotel import Room,Hotel


class ImageModel(models.Model):
    id = models.AutoField(primary_key=True, )
    img = models.ImageField(verbose_name='图片')
    class Meta:
        app_label = 'chaolife'
        abstract = True


class RoomImg(ImageModel):
    related_name = 'room_imgs'
    room = models.ForeignKey(Room, verbose_name='房型', related_name=related_name)

    def __unicode__(self):
        return self.room.name + ':' + self.img_url

    def __str__(self):
        return self.__unicode__()


class HotelImg(ImageModel):
    relation_name = 'hotel_imgs'
    hotel = models.ForeignKey(Hotel,verbose_name='房型',related_name=relation_name)

    class Meta:
        app_label = 'chaolife'
        verbose_name = '房间展示图片'
    def __str__(self):
        return self.hotel.name + ':' + self.img.url


class SplashImg(TimeStampMixin,ImageModel):
    version = models.CharField(max_length=10,verbose_name='版本',default=0.1,unique=True)
    active = models.BooleanField(default=False,verbose_name='是否在前端显示',)

    class Meta:
        verbose_name = '闪屏图'


