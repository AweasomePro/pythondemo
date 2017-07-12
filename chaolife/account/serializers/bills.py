from dynamic_rest.serializers import DynamicModelSerializer
from account.models import BillHistory

class BillHistorySerializer(DynamicModelSerializer):
    class Meta:
        model = BillHistory
        name = 'billHistory'
        plural_name = 'billHistory_set'