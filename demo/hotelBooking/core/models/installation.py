from django.db import models
from . import BaseModel
from ...utils.fiels import ListField
from hotelBooking.models import User

class Installation(BaseModel):
    badge = models.BigIntegerField(null=True,default=0,verbose_name='ios badge数')
    channels = ListField(default=[],verbose_name='订阅渠道')
    deviceProfile = models.CharField(max_length=200,default="")
    deviceToken = models.CharField(max_length=200,unique=True,null=True)
    deviceType = models.CharField(max_length=200,default="")
    installationId = models.CharField(max_length=200,unique=True,null=True,verbose_name='设备id')
    timeZone = models.CharField(max_length=200,null=True,default="")
    user = models.ForeignKey(User,null=True,default=-1,verbose_name='绑定用户')

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = "App已安装设备"
        verbose_name_plural = "设备"

    def __unicode__(self):
        return '%s-Token %s'%(self.deviceType,self.deviceToken)

    def __str__(self):
        return '%s-Token %s'%(self.deviceType,self.deviceToken)