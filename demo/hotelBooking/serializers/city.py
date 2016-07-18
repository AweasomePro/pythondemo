from hotelBooking.serializers.hotels import HotelSerializer
from hotelBooking.models.city import City
from hotelBooking.serializers.support import DynamicFieldsModelSerializer
from dynamic_rest.serializers import DynamicModelSerializer

class CitySerializer(DynamicModelSerializer):
    hotels = HotelSerializer(many=True,exclude_fields=('hotel_rooms',),embed=True)

    class Meta:
        model = City
        exclude = ('province',)