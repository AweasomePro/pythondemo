# -*- coding:utf-8 -*-
from chaolife.models.products import RoomDayState, RoomPackage
from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework import serializers
from chaolife.exceptions.exceptions import ConditionDenied
class UpdateSingleRoomDaystateSerializer(serializers.Serializer):
    state = serializers.IntegerField(max_value=1, min_value=0)
    date = serializers.DateField()

    def __init__(self, data=None, roomPackage=None):
        self.roomPackage = roomPackage
        super(UpdateSingleRoomDaystateSerializer, self).__init__(instance=None, data=data)

    def save(self, **kwargs):
        data = self.validated_data
        roomPackage = self.roomPackage
        try:
            roomDaystate = RoomDayState.objects.get(roomPackage=roomPackage,
                                    date=data['date'],)
            roomDaystate.state = self.validated_data['state']
            roomDaystate.save(update_fields=('state',))
        except RoomDayState.DoesNotExist:
            raise ConditionDenied('日期非法')
        roomDaystate.refresh_from_db()
        return roomDaystate

class UpdateRoomDayStatesSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    s_point = serializers.IntegerField(min_value=100)
    s_price = serializers.IntegerField(min_value=100)
    d_point = serializers.IntegerField(min_value=100)
    d_price = serializers.IntegerField(min_value=100)
    # state = serializers.IntegerField(max_value=1, min_value=0)

    def __init__(self,data=None, roomPackage=None ):
        self.roomPackage = roomPackage
        super(UpdateRoomDayStatesSerializer, self).__init__(instance=None, data=data)

    def validate(self, attrs):
        price_type = self.roomPackage.price_type
        if price_type == RoomPackage.PRICE_SAME and attrs['s_price']!=attrs['d_price']:
                raise serializers.ValidationError(detail='同价房型，单双价格必须相同')
        return attrs


    def save(self, **kwargs):
        data = self.validated_data
        roomPackage = self.roomPackage
        count = RoomDayState.objects.filter(roomPackage=roomPackage,
                                    date__gte=data['start_date'], date__lt=data['end_date']).update(
            s_point = data['s_point'],
            s_price = data['s_price'],
            d_price = data['d_price'],
            d_point = data['d_point'],
        )
        return count
