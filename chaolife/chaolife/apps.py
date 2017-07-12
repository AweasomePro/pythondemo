# -*- coding:utf-8 -*-
from django.apps import AppConfig


class HotelbookingConfig(AppConfig):
    app_label = 'chaolife'
    name = 'chaolife'
    def ready(self):
        from . import signals
