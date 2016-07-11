from rest_framework.decorators import api_view, throttle_classes, authentication_classes, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from hotelBooking import HotelPackageOrder
from hotelBooking.core.order_creator.utils import add_hotel_order
from hotelBooking.core.serializers.orders import CustomerOrderSerializer
from hotelBooking.permissions.orderpermissions import IsOrderCustomer
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse
from hotelBooking import wrapper_response_dict

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


class CustomerOrderActionAPIView(APIView):
    serializer_class = CustomerOrderSerializer
    queryset = HotelPackageOrder.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,IsOrderCustomer)

    ACTION_CANCEL = 'cancel'

    def post(self,request):
        action = request.POST.get('action',None)
        if action == CustomerOrderActionAPIView.ACTION_CANCEL:
            #  用户取消订单
            hotelpackageorder = request.order
            request.order.customer_cancel_order(request.user)
            request.order.refresh_from_db()
            cs = CustomerOrderSerializer(hotelpackageorder)
            return Response(wrapper_response_dict(message='退订成功',data=cs.data))
        else:
            return Response(data='未知操作')


    def cancelBookOrder(self, request,):
        number = request.POST.get('number', None)
        order = HotelPackageOrder.objects.get(number=number)
        order.cancelBook(request.user)


@api_view(['GET',])
@authentication_classes([JSONWebTokenAuthentication,])
@permission_classes(IsAuthenticated,)
def book_room(request):
    pass


class HousePackageBookAPIView(APIView):
    """
    用户 订购 酒店
    权限：已登入用户
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def post(self, request, *args, **kwargs):
        # 1 .商品是否存在
        # 2. 用户积分是否够
        # 3. 扣除积分，通知代理商
        productId = request.get('productId')

        return add_hotel_order(request)

    def is_member(self,request):
        if not request.user.is_customer_member:
            return DefaultJsonResponse(res_data='你还不是会员',code=-100)

