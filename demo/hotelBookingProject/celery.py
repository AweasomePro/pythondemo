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
from celery import Celery

# set the default Django settings module for the 'celery' program.
from hotelBookingProject import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotelBookingProject.settings')

from celery import Celery
import time
app = Celery('hotelBooking',)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task
def add(x, y):
    print('start')
    time.sleep(10000)
    print('success')
    return x + y