from django.db.models import F
from dynamic_rest.fields import DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework.exceptions import ValidationError
from ..models import Invoice,InvoiceTimeLine
from chaolife.exceptions import ConditionDenied
from django.db.models import signals

class InvoceTimeLineSerializer(DynamicModelSerializer):
    class Meta:
        model = InvoiceTimeLine
        fields = ('state','create_at')




class InvoiceSerializer(DynamicModelSerializer):
    invoicetimeline_set = DynamicRelationField(serializer_class=InvoceTimeLineSerializer, many=True, embed=True,read_only=True)

    class Meta:
        model = Invoice
        name = 'invoice'
        plur_name = 'invoices'


    def validate(self, attrs):
        if self.partial == True:
            return attrs
        # 发票金额
        value = attrs['value']
        user = attrs['user']
        max_consumptions = user.customermember.consumptions - user.customermember.invoiced_consumptions
        if value > max_consumptions:
            raise ConditionDenied('发票金额,最多{}'.format(max_consumptions))
        if Invoice.objects.filter(user=user,state__in= (Invoice.STATE_REQUIRE,Invoice.STATE_ACCEPT)).exists():
            raise ConditionDenied(detail='请勿重复提交，存在申请正在审核中')
        return attrs

    def create(self, validated_data):
        if not self.partial== True:  #
            validated_data['user'].customermember.invoiced_consumptions = F('invoiced_consumptions') + validated_data['value']
            validated_data['user'].customermember.save()
        return super(InvoiceSerializer,self).create(validated_data)

