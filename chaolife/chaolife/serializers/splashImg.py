from ..models import SplashImg
from dynamic_rest.serializers import DynamicModelSerializer

class SplashImgSerializer(DynamicModelSerializer):
    class Meta:
        model = SplashImg