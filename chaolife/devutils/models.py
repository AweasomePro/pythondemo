from django.db import models
from model_utils.models import TimeStampedModel
# Create your models here.
class Apk(TimeStampedModel):

    IOS = 'ios'
    Android = 'android'
    TYPES =((IOS,'苹果'),
            (Android,'安卓'),)
    PLATFORM = ((0,"客户端"),(1,"商家端"))
    apk  = models.FileField()
    version = models.FloatField(max_length=255,verbose_name='版本号',)
    url = models.URLField(verbose_name='url',null=True,blank=True)
    version_name = models.CharField(max_length=255,verbose_name='versionName',default='versionName')
    type = models.CharField(max_length=255,choices=TYPES)
    client = models.IntegerField(verbose_name='platform 商家端(1) or 客户端(0)',choices=PLATFORM,default=0)
    des = models.TextField(max_length=500,verbose_name='版本更新详情',default='版本描述')

    class Meta:
        ordering =('type','-version')

    def __str__(self):
        return self.type+'-'+str(self.version)