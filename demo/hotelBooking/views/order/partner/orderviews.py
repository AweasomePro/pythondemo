from django.utils.decorators import method_decorator
from rest_framework.response import Response

from hotelBooking.utils.decorators import parameter_necessary
from hotelBooking.views import views,viewsets
from dynamic_rest.viewsets import DynamicModelViewSet,WithDynamicViewSetMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route,list_route
from hotelBooking.models.orders import Order,HotelPackageOrder
from hotelBooking.permissions.rolepermissions import PartnerPermission
from hotelBooking.serializers.orders import OrderSerializer, PartnerHotelPackageOrderSerializer


# from logging import l
class PartnerHotelOrderViewSet(DynamicModelViewSet):
    permission_classes = (IsAuthenticated,PartnerPermission)
    queryset = HotelPackageOrder.objects.all()
    lookup_field = 'number'

    ACTIONS = ('accept','refuse',)
    @detail_route(methods=['GET','POST'],url_path='handle')
    @method_decorator(parameter_necessary('action',))
    def handle_order(self,request,number=None):
        """
        :param request:
        :param number: 订单号
        :return:
        """
        request.get('action',None)


        return Response('success')

    def get_serializer_class(self,*args,**kwargs):

        return PartnerHotelPackageOrderSerializer