from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from dynamic_rest.viewsets import DynamicModelViewSet
from rest_framework.response import Response

from hotelBooking.core.order_creator.utils import add_hotel_order
from hotelBooking.core.serializers.orders import CustomerOrderSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from hotelBooking.core.models.products import Product, AgentRoomTypeState
from hotelBooking import HousePackage
from hotelBooking.auth.decorators import login_required_and_is_member
from hotelBooking.core.serializers.products import RoomTypeStateSerializer, HousePackageSerializer
from hotelBooking.core.utils import hotel_query_utils
from hotelBooking.core.utils.serializer_helpers import wrapper_dict
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse
from hotelBooking.core.models.orders import HotelPackageOrder,HotelPackageOrderSnapShot

class HousePackageViewSet(viewsets.GenericViewSet):
    serializer_class = HousePackageSerializer
    queryset = HousePackage.objects.all()


def is_hotel_package(product):
    return product.name == '酒店套餐'


class HousePackageStateView(DynamicModelViewSet):
    serializer_class = RoomTypeStateSerializer
    queryset = AgentRoomTypeState.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(wrapper_dict(serializer.data))

class HousePackageView(DynamicModelViewSet):
    serializer_class = HousePackageSerializer
    queryset = HousePackage.objects.all()

    def retrieve(self, request, *args, **kwargs):
        print('do retreieve')
        hotel_query_utils.query(1,0,0)

        # instance = self.get_object()
        # serializer = self.get_serializer(instance)
        # return Response(wrapper_dict(serializer.data))
        return Response('success')
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
            print(data['order'])
            new_data.append(data['order'])
        return DefaultJsonResponse(res_data={
            'orders':
                {
                    'inprocess' : new_data,
                    'finished':[],
                }})

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        state = self.request.GET.get('state')
        return queryset.filter(order__customer=user.customermember.id)


