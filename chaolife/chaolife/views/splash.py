from ..serializers import SplashImgSerializer
from ..models import SplashImg
from common.viewsets import  CustomDynamicReadOnlyModelViewSet


class SplashViewSet(CustomDynamicReadOnlyModelViewSet):
    serializer_class = SplashImgSerializer
    queryset = SplashImg.objects
    pass