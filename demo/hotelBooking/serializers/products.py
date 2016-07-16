import datetime

from drf_enum_field.serializers import EnumFieldSerializerMixin
from dynamic_rest.fields import DynamicMethodField
from dynamic_rest.serializers import DynamicModelSerializer
# class
from hotelBooking.models.products import RoomPackage, RoomDayState


class RoomTypeStateSerializer(DynamicModelSerializer):

    class Meta:
        model = RoomDayState



class RoomPackageSerializer(EnumFieldSerializerMixin , DynamicModelSerializer):
    states = DynamicMethodField(
        requires=[
            'room_roomdaystate'
        ]
    )

    def _dynamic_init(self, only_fields, include_fields, exclude_fields):
        pass
    class Meta:
        model = RoomPackage
        fields = ('breakfast','detail','default_point','default_front_price','id','states')
        # include_fields = ('breakfast','detail','default_point','default_front_price','id')

    def get_states(self, roompackage):
        states = roompackage.roompackage_daystates.filter(date__gte =datetime.datetime.today().date()).values_list('state', flat=True).order_by('date')
        # hotel_query_utils.query(0,0,1)
        print(states)
        return states




class HotelPackageBookSerializer(DynamicModelSerializer):
    class Meta:
        pass