#-*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver
from chaolife.models import RoomPackage
from chaolife.service import packageServices
from chaolife.tasks import createRoomDaysetsFormRoomPackage
from chaolife.tasks import notify_user

@receiver(post_save, sender=RoomPackage)
def on_hotel_product_create(sender,instance,created,**kwargs):
    if(created):# 如果是新创建的 roompackage 为它创建30天的状态
        roomPackage = instance
        createRoomDaysetsFormRoomPackage.delay(roomPackage.id)

