# encoding:utf-8
from datetime import timedelta, datetime
from celery.task import task
from account.models import User
from chaolife.utils import pushtuils
from message import push_message
from celery.utils.log import get_task_logger
from chaolifeProject.settings import TEST
logger = get_task_logger(__name__)


@task
def simple_notify_user(user_id,action = 'client',extra_data=None,code = 100,alert=None,must_send=False,**kwargs):
    if action == 'client':
        action = pushtuils.HOTEL_CLIENT_ACTION
    else:
        action = pushtuils.HOTEL_PARTNER_ACTION
    user = User.objects.get(id = user_id)
    installation = user.installation_set.first()
    if installation == None:
        logger.error(msg='用户{}的installation不存在，使用短信通知'.format(user.name))
        return 'faield,no installation'
    print('发送给设备号{}'.format(installation.where_json))
    push_message(
        where= installation.where_json,
        data={
            'action':action,
            'code':code,
            'alert':alert,
            'extra_data':extra_data,
            'sound':'default',
            'prod':'dev' if TEST else 'prod'
        }

    )
    return True




@task
def push(data, channels=None, push_time=None,expiration_time=None,expiration_interval=None,where=None,cql=None):
    push.send(data, channels, push_time,expiration_time,expiration_interval,where,cql)


@task
def send_email(**kwargs):
    from django.core.mail import send_mail
    send_mail(**kwargs)