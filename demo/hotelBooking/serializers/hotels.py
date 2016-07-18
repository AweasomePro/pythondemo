from dynamic_rest.fields import DynamicMethodField
from dynamic_rest.serializers import DynamicModelSerializer
from hotelBooking.models import RoomPackage
from hotelBooking.models.hotel import Hotel, Room
from hotelBooking.models.image import HotelImg, RoomImg

from hotelBooking.serializers.products import RoomPackageSerializer


class HotelImgSerializer(DynamicModelSerializer):

    class Meta:
        model = HotelImg
        name = 'hotel_img'
        exclude =()


class RoomImgSerializer(DynamicModelSerializer):

    class Meta:
        model = RoomImg
        exclude_fields=('id',)

from rest_framework.serializers import ModelSerializer

class RoomPackageSerializer2(ModelSerializer):
    class Meta:
        model = RoomPackage
class RoomSerializer(DynamicModelSerializer):
    # roomPackages = RoomPackageSerializer(many=True,include_fields=('id',))
    roomPackages = DynamicMethodField()
    room_imgs = RoomImgSerializer(many=True, embed=True)
    class Meta:
        model = Room

    def get_roomPackages(self,room):
        room.roomPackages.all()
        rooms = room.roomPackages.all()
        rs  = RoomPackageSerializer(rooms,many=True,)
        print(room)
        return rs.data

class HotelSerializer(DynamicModelSerializer):
    hotel_imgs = HotelImgSerializer(embed=True,many=True,exclude_fields=('id','hotel'))
    # hotel_rooms = RoomSerializer(many=True, embed=True)
    types = DynamicMethodField()
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
        exclude =('agent',)