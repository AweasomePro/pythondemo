# -*- coding:utf-8 -*-
from django.apps import AppConfig


class SmsConfig(AppConfig):
    app_label = 'sms'
    name = 'sms'

    def ready(self):
        from . import signals

