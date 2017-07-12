from common.serializers import CustomModelSerializer
from .models import Apk


class ApkSerializer(CustomModelSerializer):
    class Meta:
        model = Apk
