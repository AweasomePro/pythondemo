from common.viewsets import CustomDynamicReadOnlyModelViewSet
from ..serializers.sharenotify import ShareNotifySerializer
from ..models import ShareNotify

class ShareNotifyViewSet(CustomDynamicReadOnlyModelViewSet):
    serializer_class = ShareNotifySerializer
    queryset = ShareNotify.objects.all()

