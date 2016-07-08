from hotelBooking import City
from hotelBooking.core.serializers.hotels import HotelSerializer
from hotelBooking.core.serializers.support import DynamicFieldsModelSerializer


class CitySerializer(DynamicFieldsModelSerializer):
    hotels = HotelSerializer(many=True)

    class Meta:
        model = City
        exclude = ('province',)