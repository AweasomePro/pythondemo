from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from hotelBooking.core.order_creator.utils import add_hotel_order
from hotelBooking.core.serializers.orders import CustomerOrderSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from hotelBooking.core.models.products import Product
from hotelBooking import HousePackage
from hotelBooking.auth.decorators import login_required_and_is_member
from hotelBooking.serializers import HousePackageSerializer
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse
from hotelBooking.core.models.orders import HotelPackageOrder,HotelPackageOrderSnapShot

class HousePackageViewSet(viewsets.GenericViewSet):
    serializer_class = HousePackageSerializer
    queryset = HousePackage.objects.all()


def is_hotel_package(product):
    return product.name == '酒店套餐'


class HousePackageBookAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        return add_hotel_order(request)

    def is_member(self,request):
        if not request.user.is_customer_member:
            return DefaultJsonResponse(res_data='你还不是会员',code=-100)

    def point_is_match(self,user):
        if (user.point < 10):
            pass

class CustomerHotelBookOrderList(ReadOnlyModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = HotelPackageOrder.objects.all()
    serializer_class = CustomerOrderSerializer

    def list(self, request, *args, **kwargs):
        serlaizer_datas = CustomerOrderSerializer(self.get_queryset().all(), many=True).data
        new_data = []
        for data in serlaizer_datas:
            snapshopt = data.pop('hotelpackageordersnapshot')
            type(data['order'])
            data['order']['snapshot'] = snapshopt

            new_data.append(data['order'])
        return DefaultJsonResponse(res_data={'orders':[{'all' : serlaizer_datas}]})

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        state = self.request.GET.get('state')
        return queryset.filter(order__customer=user.customermember.id)


