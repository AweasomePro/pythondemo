from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework import serializers

from hotelBooking import HotelImg,HouseImg,House,Hotel
from hotelBooking.core.serializers.products import HousePackageSerializer


class HotelImgSerializer(DynamicModelSerializer):

    class Meta:
        model = HotelImg
        name = 'hotel_img'
        exclude =()


class HouseImgSerializer(DynamicModelSerializer):

    class Meta:
        model = HouseImg
        exclude_fields=('id',)

class HouseSerializer(DynamicModelSerializer):
    house_imgs = HouseImgSerializer(many=True,embed=True)
    housePackages = HousePackageSerializer(many=True,exclude_fields=('house','product'),embed=True)
    class Meta:
        model = House


class HotelSerializer(DynamicModelSerializer):
    # hotel_imgs = HotelImgSerializer(many=True)
    # hotel_houses = HouseSerializer(many=True)
    hotel_imgs = HotelImgSerializer(embed=True,many=True,exclude_fields=('id','hotel'))
    hotel_houses = HouseSerializer(many=True,embed=True)
    class Meta:
        model = Hotel
        name = 'hotel'