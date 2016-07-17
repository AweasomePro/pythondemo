from dynamic_rest.fields import DynamicMethodField
from dynamic_rest.serializers import DynamicModelSerializer
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

# class RoomTypeSerializer(DynamicModelSerializer):
#     class Meta:
#         model = Room
#         exclude_fields=('id',)

class RoomSerializer(DynamicModelSerializer):
    room_imgs = RoomImgSerializer(many=True, embed=True)
    roomPackages = RoomPackageSerializer(many=True, exclude_fields=('room',), embed=True)
    class Meta:
        model = Room

class HotelSerializer(DynamicModelSerializer):
    # hotel_imgs = HotelImgSerializer(many=True)
    # hotel_rooms = RoomSerializer(many=True)
    hotel_imgs = HotelImgSerializer(embed=True,many=True,exclude_fields=('id','hotel'))
    hotel_rooms = RoomSerializer(many=True, embed=True)
    # types = RoomTypeSerializer(many=True,embed=True)
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