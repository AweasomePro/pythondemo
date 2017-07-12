# -*- coding:utf-8 -*-
from django.apps import AppConfig


class PayConfig(AppConfig):
    app_label = 'pay'
    name = 'pay'

    def ready(self):
        from . import signals

