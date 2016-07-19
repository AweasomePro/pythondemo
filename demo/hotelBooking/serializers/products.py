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

from hotelBooking.models import TestModel

class TestSerializer(DynamicModelSerializer):
    class Meta:
        model = TestModel
class RoomPackageSerializer(EnumFieldSerializerMixin , DynamicModelSerializer):

    roomstates = RoomDayStateSerializer(many=True,embed=True)

    class Meta(ProductSerializer.Meta):
        model = RoomPackage
        fields = ('id','breakfast','extra','default_point','default_front_price','created_on','roomstates',)

    # def get_states(self, roompackage):
        # context = self.context
        # startdate = context.pop('startdate',None)
        # print('---------startdate is {}'.format(startdate))
        # enddate = context.pop('enddate',None)
        # states = roompackage.roomstates.filter(date__gte =startdate, date_lt=enddate).values_list('state', flat=True).order_by('date')
        # states = roompackage.roomstates
        # return states


class HotelPackageBookSerializer(DynamicModelSerializer):
    class Meta:
        pass