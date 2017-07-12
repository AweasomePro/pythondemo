from common.serializers import CustomModelSerializer
from ..models import ShareNotify

class ShareNotifySerializer(CustomModelSerializer):
    class Meta:
        model = ShareNotify