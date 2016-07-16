from hotelBooking.serializers.city import CitySerializer

from hotelBooking.models.province import Province
from hotelBooking.serializers.support import DynamicFieldsModelSerializer


class ProvinceSerializer(DynamicFieldsModelSerializer):
    citys = CitySerializer(many=True,excludes=('hotels',))

    class Meta:
        model= Province