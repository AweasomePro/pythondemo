from hotelBooking.serializers.hotels import HotelSerializer

from hotelBooking.models.city import City
from hotelBooking.serializers.support import DynamicFieldsModelSerializer


class CitySerializer(DynamicFieldsModelSerializer):
    hotels = HotelSerializer(many=True)

    class Meta:
        model = City
        exclude = ('province',)