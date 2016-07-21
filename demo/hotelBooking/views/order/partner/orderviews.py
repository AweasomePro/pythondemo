from hotelBooking.views import views,viewsets
from dynamic_rest.viewsets import DynamicModelViewSet,WithDynamicViewSetMixin
from rest_framework.permissions import IsAuthenticated
from hotelBooking.models.orders import Order
from hotelBooking.permissions.rolepermissions import PartnerPermission
from hotelBooking.serializers.orders import OrderSerializer
# from logging import l
class OrderViewSet(DynamicModelViewSet):
    permission_classes = (IsAuthenticated,PartnerPermission)
    queryset = Order.objects.all()

    def get_serializer_class(self,*args,**kwargs):

        return OrderSerializer