from django.db import models
from ..models.city import  City
from . import BaseModel
class Hotel(models.Model):

    # 指定 主键 primary_key =True
    id = models.AutoField(primary_key=True)
    city = models.ForeignKey(City,verbose_name='所在城市',related_name='hotels')
    name = models.CharField(max_length=200,null=False,verbose_name='酒店名')
    address = models.CharField(max_length=255,null=False,verbose_name='地址')
    introduce = models.TextField(max_length=255,verbose_name='介绍')
    contact_phone = models.CharField(max_length=255,verbose_name='联系电话')

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = "酒店"
        verbose_name_plural = "酒店"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


# class RoomType(models.Model):
#     hotel = models.ForeignKey(Hotel,related_name='room_types')
#     type_name = models.CharField(blank=False)
#     can_book =models.BooleanField(default=True)

class House(BaseModel):
    """
    这个类表示发布的房源信息
    """
    id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(Hotel,verbose_name='所属酒店',related_name='hotel_houses')
    name = models.CharField(max_length=255,default='未定义房型名',blank=False,verbose_name='房型')

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = "房型"
        verbose_name_plural = "房型"

    def __unicode__(self):
        return self.name + ''

    def __str__(self):
        return self.name + ''

# class HousePackage(Product):
#     class Meta:
#         app_label = 'hotelBooking'
#         verbose_name = "套餐"
#         verbose_name_plural = "套餐"
#
#     HOUSE_STATE_CHOICES = (
#         ('1','充沛'),
#         ('2','满房')
#     )
#     house = models.ForeignKey(House,verbose_name='房型',related_name='housePackages')
#     package_name = models.CharField(max_length=255,default='套餐名',blank=False,verbose_name='套餐名')
#     need_point = models.IntegerField(verbose_name='所需积分')
#     package_state = models.CharField(max_length=255, choices=HOUSE_STATE_CHOICES, default=HOUSE_STATE_CHOICES[0][1])
#     detail = models.TextField()