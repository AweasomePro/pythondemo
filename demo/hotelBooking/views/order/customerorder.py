from django.db import transaction
from django.utils.decorators import method_decorator
from guardian.core import ObjectPermissionChecker
from guardian.decorators import permission_required
from rest_framework.decorators import api_view, throttle_classes, authentication_classes, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from hotelBooking import HotelPackageOrder
from hotelBooking.core.order_creator.utils import add_hotel_order, generateHotelPackageProductOrder
from hotelBooking.core.serializers.orders import CustomerOrderSerializer
from hotelBooking.permissions.orderpermissions import IsOrderCustomer
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse
from hotelBooking import wrapper_response_dict
from hotelBooking.models import User
from hotelBooking.core.models.products import HousePackage,Product
from hotelBooking.utils.decorators import parameter_necessary


class CustomerHotelBookOrderList(ReadOnlyModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = HotelPackageOrder.objects.all()
    serializer_class = CustomerOrderSerializer

    def list(self, request, *args, **kwargs):
        serlaizer_datas = CustomerOrderSerializer(self.get_queryset().all(), many=True).data
        # new_data = []
        # for data in serlaizer_datas:
        #     snapshopt = data.pop('hotelpackageordersnapshot')
        #     type(data['order'])
        #     data['order']['snapshot'] = snapshopt
        #     print(data['order'])
        #     new_data.append(data['order'])
        inprocess_set = self.get_inproccess_querset()
        finished_set = self.get_finished_queryset()
        return DefaultJsonResponse(res_data={
            'orders':
                {
                    'inprocess' : CustomerOrderSerializer(inprocess_set.all(),many=True).data,
                    'finished':CustomerOrderSerializer(finished_set.all(),many=True).data,
                }})

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        state = self.request.GET.get('state')
        return queryset.filter(customer=user)

    def get_finished_queryset(self):
        return self.queryset.filter(customer=self.request.user,closed=True)

    def get_inproccess_querset(self):
        return self.queryset.filter(customer=self.request.user,closed=False)


# url is  order/customer
class CustomerOrderActionAPIView(APIView):
    serializer_class = CustomerOrderSerializer
    queryset = HotelPackageOrder.objects.all()

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    ACTION_CANCEL = 'cancel'


    def post(self,request):
        action = request.POST.get('action',None)
        number = request.POST.get('number', None)
        if number:
            request.number = number
            try:
                order = HotelPackageOrder.objects.get(number=number)
                request.order = order
                print('request user is {}'.format(request.user.name))
                print('order customer is {}'.format(request.order.customer))
            except HotelPackageOrder.DoesNotExist:
                return Response('error number')

        checker = ObjectPermissionChecker(request.user)
        print(checker.has_perm('hotelpackageorder.change_process_state', order))
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

class HousePackageBookAPIView(APIView):
    """
    用户 订购 酒店
    权限：已登入用户
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic()
    @method_decorator(parameter_necessary('productId','checkinTime','checkoutTime'))
    
    def post(self, request, *args, **kwargs):
        # 1 .商品是否存在
        # 2. 用户积分是否够
        # 3. 是否在区间存在已购订单
        # 3. 扣除积分，通知代理商
        user = request.user
        productId = kwargs.get('productId')
        checkinTime = kwargs.get('checkinTime')
        checkoutTime = kwargs.get('checkoutTime')

        # check id 是否真实
        try:
            house_package = HousePackage.objects.get(id=productId)
        except Product.DoesNotExist:
            return DefaultJsonResponse(message='不存在该商品', code=403)

        # check 在区间是否存在订单
        exist = HotelPackageOrder.objects.filter(customer=user,checkin_time__lte=checkinTime,checkout_time__gte=checkinTime).exists()
        if exist:
            return Response(wrapper_response_dict(code=-100,message='存在订单,请先取消'))

        # check 预订时间是否准确
        check_validate_checkTime(house_package,checkinTime,checkoutTime)

        # check 积分是否够
        if(user.point< house_package.need_point):
            return Response(wrapper_response_dict(code=-100,message='积分不够,充值去 - -'))

        # check point 是否足够
        request_notes = '需要wifi'

        hotelPackageOrder = generateHotelPackageProductOrder(request, user, house_package, request_notes, checkinTime,
                                                             checkoutTime)
        serializer = CustomerOrderSerializer(hotelPackageOrder)

        return DefaultJsonResponse(res_data=serializer.data,message='预订成功')



def check_point_enough_book(user,house_package):
    if user.point >= house_package:
        return True
    else:
        return False

def check_validate_checkTime(product,checkinTime,checkoutTime):
    pass