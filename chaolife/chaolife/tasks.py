# -*- coding:utf-8 -*-
from datetime import timedelta, datetime
from celery.schedules import crontab
from celery.task import task
from celery.task.base import periodic_task
from django.db import transaction
from django.db.models import Q

from account.models import Installation
from chaolife.models.products import RoomDayState
from chaolife.models.products import RoomPackage
from account.models import User
from chaolife.utils import pushtuils
from message import push_message_to_partner, push_message_to_client
from celery.utils.log import get_task_logger
from chaolifeProject.settings import TEST

logger = get_task_logger(__name__)


def notify_via_installtion(installation, client_action, extra_data='', code=100, alert=''):
    if Installation.CHANNELS_PARTNER in installation.channels:
        push_message_to_partner(
            where=installation.where_json,
            data={
                'action': client_action,
                'code': code,
                'alert': alert,
                'extra_data': extra_data,
                'sound': 'default',
                'prod': 'dev' if TEST else 'prod'
            }
        )
    else:
        push_message_to_client(
            where=installation.where_json,
            data={
                'action': client_action,
                'code': code,
                'alert': alert,
                'extra_data': extra_data,
                'sound': 'default',
                'prod': 'dev' if TEST else 'prod'
            }
        )


@task
def notify_user(user_id, extra_data='', code=100, alert='', client_action=pushtuils.HOTEL_CLIENT_ACTION):
    user = User.objects.get(id=user_id)
    installation = user.installation_set.filter(active=True).first()
    assert installation, ('没找到{}的installation'.format(user))
    push_message_to_client(
        where=installation.where_json,
        data={
            'action': client_action,
            'code': code,
            'alert': alert,
            'extra_data': extra_data,
            'sound': 'default',
            'prod': 'dev' if TEST else 'prod'
        }
    )


@task
def notify_partner(user_id, extra_data='', alert='', ):
    installation_set = Installation.partner_installations(user=User.objects.get(id=user_id))
    print('得到结果数量{}'.format(len(installation_set)))
    if bool(installation_set):
        for installation in installation_set:
            print('通知:  ')
            notify_via_installtion(installation, client_action=pushtuils.HOTEL_PARTNER_ACTION, extra_data=extra_data,
                                   alert=alert)


@task
def notify_customer(user_id, extra_data='', alert=None, ):
    installation_set = Installation.client_installations(user=User.objects.get(id=user_id))
    if bool(installation_set):
        for installation in installation_set:
            notify_via_installtion(installation, client_action=pushtuils.HOTEL_CLIENT_ACTION, extra_data=extra_data,
                                   alert=alert)


@task
def push(data, channels=None, push_time=None, expiration_time=None, expiration_interval=None, where=None, cql=None):
    push.send(data, channels, push_time, expiration_time, expiration_interval, where, cql)


@periodic_task(run_every=(crontab(minute=2)), name='check_package_task')
@transaction.atomic()
def checkHousePackageState():
    # 该任务在服务器重启 或者 是每天0点运行
    # delete all expire date state
    today = datetime.today().date()
    RoomDayState.objects.all().filter(Q(date__lt=today) | Q(date__gte=today + timedelta(days=29))).delete()
    # 检查所有的housepackage 的states 的数量，不够的则添加
    print('得到执行')
    logger.log(level=1, msg='start work')
    save_object = []
    for roompackage in RoomPackage.objects.prefetch_related('roomstates', ).all():
        roomstate = roompackage.roomstates.all().last()
        if roomstate is not None and roomstate.date < today + timedelta(days=29):
            roomstate.pk = None
            roomstate.date = roomstate.date + timedelta(days=1)
            save_object.append(roomstate)
        else:
            from chaolife.service.packageServices import createRoomDaysFormRoomPackage
            createRoomDaysetsFormRoomPackage(roompackage.id)
    RoomDayState.objects.bulk_create(save_object)


@task
def createRoomDaysetsFormRoomPackage(roomPackageId):
    roomPackage = RoomPackage.objects.get(id=roomPackageId)
    from chaolife.service.packageServices import createRoomDaysFormRoomPackage
    if (roomPackage.roomstates.count() == 0):
        createRoomDaysFormRoomPackage(roomPackage)
        return {'result': 'success'}
