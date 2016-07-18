import datetime

from drf_enum_field.serializers import EnumFieldSerializerMixin
from dynamic_rest.fields import DynamicMethodField
from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework import serializers
# class
from hotelBooking.models.products import RoomPackage, RoomDayState, Product


class RoomDayStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomDayState
        fields =('date',)

class ProductSerializer(DynamicModelSerializer):
    class Meta:
        model = Product

class RoomPackageSerializer(EnumFieldSerializerMixin , DynamicModelSerializer):
    states = DynamicMethodField(
    )
    # roomstates = RoomDayStateSerializer(many=True,)

    def _dynamic_init(self, only_fields, include_fields, exclude_fields):
        pass

    class Meta(ProductSerializer.Meta):
        model = RoomPackage
        fields = ('id','breakfast','extra','default_point','default_front_price','created_on','states',)
        # include_fields = ('breakfast','detail','default_point','default_front_price','id')

    def get_states(self, roompackage):
        states = roompackage.roomstates.filter(date__gte =datetime.datetime.today().date()).values_list('state', flat=True).order_by('date')
        # hotel_query_utils.query(0,0,1)
        print(states)
        return states


class HotelPackageBookSerializer(DynamicModelSerializer):
    class Meta:
        pass