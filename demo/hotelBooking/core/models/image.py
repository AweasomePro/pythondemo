from django.db import models
from ..models.hotel import House,Hotel
from . import python_2_unicode_compatible

class ImageModel(models.Model):
    id = models.AutoField(primary_key=True, )
    img_url = models.CharField(max_length=250, verbose_name='图片地址', )
    class Meta:
        app_label = 'hotelBooking'
        abstract = True

class HouseImg(ImageModel):
    relation_name = 'house_imgs'
    house = models.ForeignKey(House,verbose_name='房型',related_name=relation_name)

    def __unicode__(self):
        return self.house.name + ':' + self.img_url

    def __str__(self):
        return self.__unicode__()

@python_2_unicode_compatible
class HotelImg(ImageModel):
    relation_name = 'hotel_imgs'
    hotel = models.ForeignKey(Hotel,verbose_name='房型',related_name=relation_name)

    def __str__(self):
        return self.house.name + ':' + self.img_url