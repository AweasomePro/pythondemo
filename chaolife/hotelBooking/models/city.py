from django.db import models
from model_utils.models import StatusModel
from ..models.province import Province

class City(models.Model):
    # id = models.AutoField(primary_key=True)
    code = models.IntegerField(unique=True,primary_key=True,verbose_name='城市代号')
    name = models.CharField(max_length=200, null=False,verbose_name='城市')
    province = models.ForeignKey(Province,verbose_name='所属省份',related_name='citys')
    logo = models.URLField(blank=False,default='http://img4.imgtn.bdimg.com/it/u=2524053065,1600155239&fm=21&gp=0.jpg',verbose_name='城市Logo图')
    class Meta:
        app_label = 'hotelBooking'
        verbose_name = "城市"
        verbose_name_plural = "城市"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name