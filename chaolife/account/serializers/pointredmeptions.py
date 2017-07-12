from account.models import User
from ..models import PointRedemption,PointRedemptionLog
from ..models import BillHistory
from rest_framework import serializers
from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields import DynamicRelationField
from chaolife.exceptions import ConditionDenied


class PointRedemptionLogSerializer(DynamicModelSerializer):
    class Meta:
        model =PointRedemptionLog
        fields = ('created','state')


class PointRedemptionSerializer(DynamicModelSerializer):
    pointredemptionlog_set =DynamicRelationField(serializer_class=PointRedemptionLogSerializer,many=True,embed=True)
    state = serializers.IntegerField(required=False,read_only=True,default=1)

    class Meta:
        model = PointRedemption
        name = 'pointRedemption'
        plural_name = 'pointRedemptions'

    def validate(self, attrs):
        points = attrs['points']
        user = User.objects.prefetch_related('partnermember').select_for_update().get(id = attrs['user'].id)
        self.user = user
        if points > user.partnermember.points :
            raise ConditionDenied(detail='最多提现{}'.format( user.partnermember.points) )
        if points < 5000:
            raise ConditionDenied(detail='积分5000起提')
        if points > user.partnermember.invoice:
            raise  ConditionDenied(detail='可开发票额度不足，目前为{}'.format(user.partnermember.invoice))
        return attrs

    def create(self, validated_data):
        point_redemption = PointRedemption(state=PointRedemption.STATE_REQUIRE,user=validated_data['user'],points= validated_data['points'],card=validated_data['card'])
        #做记录，同时扣除积分
        BillHistory.createForRedmption(point_redemption)
        point_redemption.save()
        return point_redemption
