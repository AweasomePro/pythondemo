from dynamic_rest.fields import DynamicMethodField
from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest import serializers as dynamic_serializers
from rest_framework import serializers as rest_serializers
from hotelBooking.models import RoomPackage
from hotelBooking.models.hotel import Hotel, Room
from hotelBooking.models.image import HotelImg, RoomImg

from hotelBooking.serializers.products import RoomPackageSerializer
from rest_framework.serializers import ModelSerializer


class HotelImgSerializer(DynamicModelSerializer):

    class Meta:
        model = HotelImg
        name = 'hotel_img'
        exclude =('id','hotel',)


class RoomImgSerializer(DynamicModelSerializer):

    class Meta:
        model = RoomImg
        exclude_fields=('id',)



class WithDayFilterMixin():
    def __init__(self,startdate=None,enddate=None,**kwargs):
        print('kwargs is {}'.format(kwargs))
        self.startdate = startdate
        self.enddate = enddate
        super(WithDayFilterMixin, self).__init__(**kwargs)

class RoomSerializer(DynamicModelSerializer):
    roomPackages = RoomPackageSerializer(many=True,embed=True)
    room_imgs = RoomImgSerializer(many=True, embed=True)

    class Meta:
        model = Room
        name = 'room'
        plural_name = 'roomtypes'
        exclude = ('checked','active','hotel',)




class HotelSerializer(DynamicModelSerializer):
    hotel_imgs = HotelImgSerializer(read_only=True, many=True, embed=True)
    min_price = DynamicMethodField()

    def get_types(self,hotel):
        types = hotel.hotel_rooms.values('id','name')
        print(types)
        return types

    def get_min_price(self,hotel):
        res = hotel.roompackage_set.values('default_front_price', 'default_point').order_by('-default_front_price').last()
        return res

    class Meta:
        model = Hotel
        name = 'hotel'
        exclude =('agent','city',)

class HotelDetailSerializer(DynamicModelSerializer):

    """
    根据主键
    需要显示所有的room
    """
    rooms = rest_serializers.SerializerMethodField('room_details')
    hotel_imgs = HotelImgSerializer(read_only=True,many=True,embed=True)

    def room_details(self,hotel):
        data = RoomSerializer(hotel.hotel_rooms,many=True,include_fields=('name',),embed=True).data
        return data

    class Meta:
        model = Hotel
        name = 'hotel'

class HotelTypeSerializer(DynamicModelSerializer):
    # types = DynamicMethodField()

    def get_types(self, hotel):
        types = hotel.hotel_rooms.values('id', 'name')
        return types

    class Meta:
        model = Hotel
        name = 'roomtype'
        plural_name = 'roomtypes'

        fields = ('agent', 'city',)