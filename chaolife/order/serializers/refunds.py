from common.serializers import CustomModelSerializer
from ..models import OrderRefund


class RefundOrderSerializer(CustomModelSerializer):

    class Meta:
        model = OrderRefund
        name = 'refundorder'
        plur_name = 'refundorders'