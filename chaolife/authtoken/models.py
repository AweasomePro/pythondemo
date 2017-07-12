import binascii
import os

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from common import exceptions
# Prior to Django 1.5, the AUTH_USER_MODEL setting does not exist.
# Note that we don't perform this code in the compat module due to
# bug report #1297
# See: https://github.com/tomchristie/django-rest-framework/issues/1297
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


def hook_platform(platform):
    if platform == 'anroid':
        return 1
    elif platform == 'ios':
        return 2
    else:
        return -1



@python_2_unicode_compatible
class Token(models.Model):
    TYPE_CLIENT = 1
    TYPE_BUSINESS = 2
    TYPE_CHOICE = ((TYPE_CLIENT, 'client'), (TYPE_BUSINESS, 'business'),)
    """
    The default authorization token model.
    """
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='auth_token')
    created = models.DateTimeField(auto_now_add=True)
    client_type = models.SmallIntegerField(choices=TYPE_CHOICE,null=False,blank=True)

    partner_max_connection = 3 # 商家端最多连接数
    customer_max_connection = 1 # 客户端最多连接数

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/tomchristie/django-rest-framework/issues/705
        abstract = 'authtoken' not in settings.INSTALLED_APPS
        ordering =('user','-created',)


    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    @staticmethod
    def create_for_mobile_client(user, client_type):
        if client_type  == 'client':
            from account.models.user import User
            tokens = user.auth_token.filter(client_type = Token.TYPE_CLIENT).all()
            if tokens:
                tokens.delete()
            return Token.objects.create(user=user,client_type=Token.TYPE_CLIENT)
        elif client_type == 'business':
            if  user.auth_token.filter(client_type = Token.TYPE_BUSINESS).count() >= 3:
                user.auth_token.filter(client_type = Token.TYPE_BUSINESS).last().delete()
            return Token.objects.create(user=user,client_type=Token.TYPE_BUSINESS)

    def __str__(self):
        return self.key
