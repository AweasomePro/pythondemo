from hotelBooking import HousePackage
from hotelBooking.core.serializers.support import DynamicFieldsModelSerializer


class HousePackageSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = HousePackage
        exclude=('id',)

class HotelPackageBookSerializer(DynamicFieldsModelSerializer):

    class Meta:
        pass