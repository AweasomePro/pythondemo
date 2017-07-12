from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from authtoken.models import Token
from common.fiels import ListField
from .user import User



class Installation(models.Model):

    CHANNELS_CUSTOMER = "customer"
    CHANNELS_PARTNER = "Hpartner"
    user = models.ForeignKey(User,null=True,verbose_name='绑定用户',to_field='phone_number',db_index=True)
    # token = models.OneToOneField(Token,on_delete=models.CASCADE,null=True)
    valid = models.BooleanField(default=True)
    timeZone = models.CharField(max_length=200,default=timezone.now)
    channels = ListField(default=["customer",],verbose_name='订阅渠道',null=True)
    deviceToken = models.CharField(max_length=200,null=True)
    installationId = models.CharField(max_length=200,null=True,verbose_name='设备id')
    deviceType = models.CharField(max_length=200,default="android")
    badge = models.BigIntegerField(default=0,verbose_name='ios badge数')
    deviceProfile = models.CharField(max_length=200,default="")
    active = models.BooleanField(_('active?'),default=True)

    class Meta:
        app_label = 'account'
        verbose_name = "App已安装设备"
        verbose_name_plural = "设备"
        ordering = ('user','-timeZone')

    def __unicode__(self):
        return '%s-Token %s'%(self.deviceType,self.deviceToken)

    def __str__(self):
        return '%s-Token %s'%(self.deviceType,self.deviceToken)

    @property
    def key(self):
        if(self.deviceType == 'android'):
            return {'installationId':self.installationId}
        else:
            return {'deviceToken':self.deviceToken}

    @property
    def where_json(self):
        if (self.deviceType == 'android'):
            return {'installationId': self.installationId}
        else:
            return {'deviceToken': self.deviceToken,"deviceType":"ios"}

    @classmethod
    def client_installations(Installatoin, user):
        installation_set = []
        for installation in Installatoin.objects.filter(user=user ,active=True).iterator():
            if Installation.CHANNELS_CUSTOMER in  installation.channels:
                installation_set.append(installation)
        return installation_set

    @classmethod
    def partner_installations(Installatoin, user):
        installation_set = []
        for installation in Installatoin.objects.filter(user=user, active=True).iterator():
            if Installation.CHANNELS_PARTNER in installation.channels:
                installation_set.append(installation)
        return installation_set

    @staticmethod
    def check_count_limit(user):
        for installation in Installation.objects.filter(channels__contains=Installation.CHANNELS_CUSTOMER,user=user)[1:]:
            installation.delete()
        for installation in Installation.objects.filter(channels__contains=Installation.CHANNELS_PARTNER,user=user)[3:]:
            print('开始删除')
            installation.delete()

def validate_unique_deviceToken_or_null(value):
    if value != None:
        Installation.objects.update_or_create()
        pass