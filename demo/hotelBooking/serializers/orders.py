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


class CustomerOrderSerializer(DynamicModelSerializer):
    # order = OrderSerializer()
    # hotelpackageordersnapshot = HotelPackgeOrderSnapShotSerialier()

    class Meta:
        model = HotelPackageOrder
        name = 'order'
        # exclude = ('id','order')

    def to_representation(self, instance):
        print('to_presentation')
        orderDict = super(CustomerOrderSerializer,self).to_representation(instance)
        return orderDict


