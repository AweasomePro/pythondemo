from django.apps import AppConfig


class AccountConfig(AppConfig):
    app_label = 'account'
    name = 'account'

    def ready(self):
        from . import signals
