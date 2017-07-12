# -*- coding:utf-8 -*-
from django.apps import AppConfig


class CholifeWebConfig(AppConfig):
    app_label = 'chaolifeWeb'
    name = 'chaolifeWeb'

    def ready(self):
        from . import signals

