import datetime

from drf_enum_field.serializers import EnumFieldSerializerMixin
from dynamic_rest.fields import DynamicMethodField
from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.serializers import DynamicRelationField
from hotelBooking import HousePackage
# class
from hotelBooking.core.models.products import AgentRoomTypeState
from hotelBooking.core.utils import hotel_query_utils


class RoomTypeStateSerializer(DynamicModelSerializer):

    class Meta:
        model = AgentRoomTypeState



class HousePackageSerializer(EnumFieldSerializerMixin ,DynamicModelSerializer):


    states = DynamicMethodField(
        requires=[
            'house_roomstate'
        ]
    )

    def get_states(self,housepackage):
        states = housepackage.housepackage_roomstates.filter(date__gte =datetime.datetime.today().date()).values_list('state',flat=True).order_by('date')
        # hotel_query_utils.query(0,0,1)
        print(states)
        return states
    class Meta:
        model = HousePackage

# class CreateHousePackageSerializer(DynamicModelSerializer):
#     class Meta:
#         model = HousePackage


class HotelPackageBookSerializer(DynamicModelSerializer):
    class Meta:
        pass