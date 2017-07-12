from django.db import models


class ShareNotify(models.Model):
    name = models.CharField(max_length=100,verbose_name='分享的主题',primary_key=True)
    title = models.CharField(max_length=50,verbose_name='标题',null=False,blank=False)
    sub_title = models.CharField(max_length=50,verbose_name='副标题',null=True,blank=True)
    content = models.TextField(max_length=500,verbose_name='内容',null=True,blank=True)
    extra_image = models.ImageField(verbose_name='图片',null=True,blank=True)

    class Meta:
        verbose_name = '活动通知'
        verbose_name_plural = '活动通知'

    def __str__(self):
        return self.name+'-'+self.title