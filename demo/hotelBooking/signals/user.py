from django.db.models.signals import pre_delete
from django.core.signals import request_started
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(request_started)
def request_start_callback(sender,**kwargs):
    print('Request start')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)