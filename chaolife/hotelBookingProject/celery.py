from __future__ import absolute_import

# from __future__ import absolute_import
# import os
# from celery import Celery
# from django.conf import settings
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE','hotelBookingProject.settings')
# app = Celery('hotelBooking')
#
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
import os

# set the default Django settings module for the 'celery' program.
from celery import Celery
import time
from hotelBookingProject import settings
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotelBookingProject.settings')

app = Celery('hotelBooking',)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings') # 这样的做法仅仅是为了方便，我们不需要多个配置文件，直接在django settings里面配置celerly
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)  #为了重用django app，通常是在单独的tasks.py模块中定义所有任务，celery 会自动发现这些模块

app.conf.update( #  我将使用数据库作为结果存储后端，这一步会创建任务结果的相关数据库表，以及周期任务使用的数据库表，这行配置也可以直接在djanbgo setting 中设置
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json',],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=False,
)
#  debug_task 是一个打印本省request信息的任务，它使用了Celry 3.1引入的任务选项bind =true使得引用当前任务实例变得更容易
# @shared_task 装饰器能让我妈在没有具体的Celry 实例时创建任务
@app.task
def add(x, y):
    print('start')
    time.sleep(10000)
    print('success')
    return x + y

