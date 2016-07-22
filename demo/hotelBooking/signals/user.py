from django.db.models.signals import pre_delete
from django.core.signals import request_started
from django.dispatch import receiver

@receiver(request_started)
def request_start_callback(sender,**kwargs):
    print('Request start')

