from django.db.models.signals import post_save
from django.dispatch import receiver
from hotelBooking.models import RoomPackage
from hotelBooking.service import packageServices
from hotelBooking.tasks import createRoomDaysetsFormRoomPackage
@receiver(post_save, sender=RoomPackage)
def on_hotel_product_create(sender,instance,created,**kwargs):
    if(created):# 如果是新创建的 roompackage 为它创建30天的状态
        roomPackage = instance
        # todo 做double check
        createRoomDaysetsFormRoomPackage.delay(roomPackage.id)
        # try:
        #     packageServices.createRoomDaysetsFormRoomPackage(roomPackage)
        # except BaseException as e:
        #     print('出现异常 做日志处理')
