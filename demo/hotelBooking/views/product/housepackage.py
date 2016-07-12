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
from hotelBooking.core.utils.serializer_helpers import wrapper_response_dict
from hotelBooking.test.performance import fn_time
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse
from hotelBooking.core.models.orders import HotelPackageOrder,HotelPackageOrderSnapShot
from hotelBooking.models import User
from hotelBooking.core.models.houses import House
class HousePackageViewSet(viewsets.GenericViewSet):
    serializer_class = HousePackageSerializer
    queryset = HousePackage.objects.all()


class AddHousePackageView(APIView):

    def post(self, request, *args, **kwargs):
        user = User.objects.get(phone_number=15726814574)
        p = Product(owner=user)
        p.save()
        hp = HousePackage(front_price=300,need_point=10,house=House.objects.first(),product=p)
        hp.save()
        return Response(wrapper_response_dict(message='创建成功'))

@api_view(['POST',])
def create_new_hotelpackage(request):
    user = User.objects.get(phone_number=15726814574)
    p = Product(owner=user)
    p.save()
    hp = HousePackage(front_price=300, need_point=10, house=House.objects.first(), product=p)
    hp.save()
    return Response(wrapper_response_dict(message='创建成功'))


class HousePackageStateView(DynamicModelViewSet):
    serializer_class = RoomTypeStateSerializer
    queryset = AgentRoomTypeState.objects.all()
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(wrapper_response_dict(serializer.data))

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
    ACTION_BOOK = 'book'

    def post(self, request, *args, **kwargs):
        print(args)
        print(kwargs)

        return self.customer_book(request=request)


    def customer_book(self,request):
        user = request.user
        customeruser = user.customermember
        product_id = request.POST.get('productId',None)
        return add_hotel_order(request,user)





