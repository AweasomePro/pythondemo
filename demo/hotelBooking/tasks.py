# encoding:utf-8
from datetime import timedelta
from django.db import transaction
from celery.task import task
from celery.schedules import crontab
from celery.task.base import periodic_task
from hotelBookingProject.celery import app
from hotelBooking.models import User
from hotelBooking.module import push
from hotelBooking import HousePackage
from hotelBooking.core.models.products import AgentRoomTypeState

@task
def notify(phone_number, message):
    user = User.objects.get(phone_number=phone_number)
    installations = user.installation_set.filter(active=True).all()
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
    AgentRoomTypeState.objects.all().filter(date__lt=today).delete()
    # 检查所有的housepackage 的states 的数量，不够的则添加

    save_object = []
    for h in HousePackage.objects.all():
        roomstate = h.housepackage_roomstates.all().last()
        roomstate.pk = None
        roomstate.date = roomstate.date + timedelta(days=1)
        save_object.append(roomstate)
    AgentRoomTypeState.objects.bulk_create(save_object)

    sp_delete_expire = transaction.savepoint()
