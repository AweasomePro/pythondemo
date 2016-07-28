from django.db.models.signals import post_save
from django.dispatch import receiver
from hotelBooking.models import RoomPackage
from hotelBooking.service import packageServices
from hotelBooking.tasks import createRoomDaysetsFormRoomPackage
from hotelBooking.tasks import simple_notify

@receiver(post_save, sender=RoomPackage)
def on_hotel_product_create(sender,instance,created,**kwargs):
    print('是否是新创建的hotelpackage{}'.format(created))
    if(created):# 如果是新创建的 roompackage 为它创建30天的状态
        roomPackage = instance
        # todo 做double check
        print('真的要开始了')
        simple_notify.delay('15726814574','hello')
        createRoomDaysetsFormRoomPackage.delay(roomPackage.id)
        # try:
        #     packageServices.createRoomDaysetsFormRoomPackage(roomPackage)
        # except BaseException as e:
        #     print('出现异常 做日志处理')
