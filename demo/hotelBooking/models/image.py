from django.db import models
from ..models.hotel import Room,Hotel

class ImageModel(models.Model):
    id = models.AutoField(primary_key=True, )
    img = models.ImageField(verbose_name='图片')
    class Meta:
        app_label = 'hotelBooking'
        abstract = True

class RoomImg(ImageModel):
    related_name = 'room_imgs'
    room = models.ForeignKey(Room, verbose_name='房型', related_name=related_name)

    def __unicode__(self):
        return self.room.name + ':' + self.img_url

    def __str__(self):
        return self.__unicode__()

class HotelImg(ImageModel):
    relation_name = 'hotel_imgs'
    hotel = models.ForeignKey(Hotel,verbose_name='房型',related_name=relation_name)

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = '房间展示图片'
    def __str__(self):
        return self.hotel.name + ':' + self.img.url