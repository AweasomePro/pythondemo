from hotelBooking.views import views,viewsets
from dynamic_rest.viewsets import DynamicModelViewSet,WithDynamicViewSetMixin
from rest_framework.permissions import IsAuthenticated

class OrderViewSet(DynamicModelViewSet):
    permission_classes = ()
    pass