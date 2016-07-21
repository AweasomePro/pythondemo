from dynamic_rest.serializers import DynamicModelSerializer
from hotelBooking.models.orders import HotelPackageOrder, Order
from hotelBooking.serializers.support import DynamicFieldsModelSerializer


# class HotelPackgeOrderSnapShotSerialier(DynamicFieldsModelSerializer):
#     # hotel_name = serializers.CharField()
#
#     class Meta:
#         model = HotelPackageOrderSnapShot
#         exclude=('id','hotel_package_order')
#         # fields =('hotel_name','room_type_name',)


class OrderSerializer(DynamicModelSerializer):
    # number = serializers.IntegerField()
    # shipping_status = serializers.IntegerField

    class Meta:
        model = Order
        # fields = ('number','id')

class PartnerHotelPackageOrderSerializer(DynamicModelSerializer):

    class Meta:
        model = HotelPackageOrder
        exclude = ('deleted','customer',)
        name = 'orders'


class CustomerOrderSerializer(DynamicModelSerializer):

    class Meta:
        model = HotelPackageOrder
        name = 'order'
        plural_name = 'orders'




