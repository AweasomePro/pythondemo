# encoding:utf-8
from datetime import timedelta, datetime

from celery.schedules import crontab
from celery.task import task
from celery.task.base import periodic_task
from django.db import transaction
from hotelBooking.models.products import RoomDayState
from hotelBooking.models.products import RoomPackage
from hotelBooking.models.user.users import User
from hotelBooking.module import push


@task
def notify(phone_number, message):
    user = User.objects.get(phone_number=phone_number)
    installations = user.installation_set.filter(active=True).all()
    print('通知用户')
    for installation in installations:
        push.send(
            where= {'installationId':str(installation.installationId)},
            data={'alert':message}
        )

@periodic_task(run_every=(crontab(minute=2)),name='check_package_task')
@transaction.atomic()
def checkHousePackageState(today):

    # 该任务在服务器重启 或者 是每天0点运行
    # delete all expire date state
    RoomDayState.objects.all().filter(date__lt=today).delete()
    # 检查所有的housepackage 的states 的数量，不够的则添加
    print('得到执行')
    save_object = []
    for h in RoomPackage.objects.all():
        roomstate = h.housepackage_roomstates.all().last()
        if roomstate is not None:
            roomstate.pk = None
            roomstate.date = roomstate.date + timedelta(days=1)
            save_object.append(roomstate)
        else:
            owner = h.owner
            housepackage = h
            house_type = h.house
            hotel = h.house.hotel
            city = h.house.hotel.city
            day = datetime.today().date()
            for i in range(0, 30):
                print(day.strftime('%Y-%m-%d'))
                print(i)
                obj = RoomDayState(agent=owner,
                                   housePackage=housepackage,
                                   house_type=house_type,
                                   hotel=hotel,
                                   city=city,
                                   state=RoomDayState.ROOM_STATE_ENOUGH,
                                   date=day.strftime('%Y-%m-%d'))
                save_object.append(obj)
                day += timedelta(days=1)
    RoomDayState.objects.bulk_create(save_object)
    sp_delete_expire = transaction.savepoint()
