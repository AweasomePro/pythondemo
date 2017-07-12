from .models import SmsRecord
from common.serializers import CustomModelSerializer


class SmsRecordSerializer(CustomModelSerializer):

    class Meta:
        model = SmsRecord
        write_only = ('vertify_code',)
