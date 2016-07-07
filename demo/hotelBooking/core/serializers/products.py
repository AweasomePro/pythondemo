from dynamic_rest.serializers import DynamicModelSerializer

from hotelBooking import HousePackage


# class

class HousePackageSerializer(DynamicModelSerializer):

    class Meta:
        model = HousePackage
        exclude_fields=()

class HotelPackageBookSerializer(DynamicModelSerializer):
    class Meta:
        pass