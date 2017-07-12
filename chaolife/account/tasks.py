#-*- coding: utf-8 -*-
from celery.task import task
@task()
def testtask():
    from django.core.mail import send_mail
    send_mail('日志', '测试异步任务', 'chaomengshidai@agesd.com',
              ['nimdanoob@163.com', ])
    print('成功执行任务')
    return 'task is success'