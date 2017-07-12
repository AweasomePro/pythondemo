# -*- coding:utf-8 -*-
from django.apps import AppConfig


class OrderConfig(AppConfig):
    app_label = 'order'
    name = 'order'

    def ready(self):
        from . import signals

