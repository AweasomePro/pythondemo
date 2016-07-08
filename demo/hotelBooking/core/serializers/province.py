from hotelBooking import Province
from hotelBooking.core.serializers.city import CitySerializer
from hotelBooking.core.serializers.support import DynamicFieldsModelSerializer


class ProvinceSerializer(DynamicFieldsModelSerializer):
    citys = CitySerializer(many=True,excludes=('hotels',))

    class Meta:
        model= Province