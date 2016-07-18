import datetime
from rest_framework.serializers import ModelSerializer
from drf_enum_field.serializers import EnumFieldSerializerMixin
from dynamic_rest.fields import DynamicMethodField, DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer
# class
from hotelBooking.models.products import RoomPackage, RoomDayState, Product


class RoomDayStateSerializer(DynamicModelSerializer):

    class Meta:
        model = RoomDayState
        fields = ('need_point','front_price','date','state')


class ProductSerializer(DynamicModelSerializer):
    class Meta:
        model = Product

class RoomPackageSerializer(EnumFieldSerializerMixin , DynamicModelSerializer):
    # states = DynamicMethodField(
    # )

    roomstates = RoomDayStateSerializer(many=True,embed=True)

    class Meta(ProductSerializer.Meta):
        model = RoomPackage
        fields = ('id','breakfast','extra','default_point','default_front_price','created_on','roomstates')
        # include_fields = ('breakfast','detail','default_point','default_front_price','id')

    def get_states(self, roompackage):
        states = roompackage.roomstates.filter(date__gte =datetime.datetime.today().date()).values_list('state', flat=True).order_by('date')
        return states


class HotelPackageBookSerializer(DynamicModelSerializer):
    class Meta:
        pass