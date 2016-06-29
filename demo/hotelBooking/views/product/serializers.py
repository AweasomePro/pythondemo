from hotelBooking import HousePackage
from hotelBooking.serializers import DynamicFieldsModelSerializer


class HousePackageSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = HousePackage
        exclude=('id',)