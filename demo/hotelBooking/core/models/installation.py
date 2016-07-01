from django.utils import timezone

from django.db import models
from . import BaseModel
from ...utils.fiels import ListField
from hotelBooking.models import User

class Installation(BaseModel):
    valid = models.BooleanField(default=True)
    timeZone = models.CharField(max_length=200,default=timezone.now)
    channels = ListField(default=[],verbose_name='订阅渠道')
    deviceToken = models.CharField(max_length=200,null=True)
    deviceType = models.CharField(max_length=200,default="android")
    installationId = models.CharField(max_length=200,null=True,verbose_name='设备id')
    badge = models.BigIntegerField(default=0,verbose_name='ios badge数')
    deviceProfile = models.CharField(max_length=200,default="")
    user = models.ForeignKey(User,null=True,verbose_name='绑定用户')

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = "App已安装设备"
        verbose_name_plural = "设备"

    def __unicode__(self):
        return '%s-Token %s'%(self.deviceType,self.deviceToken)

    def __str__(self):
        return '%s-Token %s'%(self.deviceType,self.deviceToken)