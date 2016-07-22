from django.db import transaction
from datetime import datetime
from django.utils.decorators import method_decorator
from guardian.core import ObjectPermissionChecker
from guardian.shortcuts import assign_perm
from rest_framework.decorators import detail_route

from hotelBooking.core.exceptions import PointNotEnough, ConditionDenied
from hotelBooking.core.utils.serializer_helpers import wrapper_response_dict
from hotelBooking.models.orders import HotelPackageOrder, HotelPackageOrderItem
from hotelBooking.models.plugins import HotelOrderNumberGenerator
from hotelBooking.models.products import RoomPackage,Product,RoomDayState
from hotelBooking.pagination import StandardResultsSetPagination
from hotelBooking.serializers import CustomerOrderSerializer
from hotelBooking.utils import dateutils
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse, JSONWrappedResponse
from hotelBooking.utils.decorators import parameter_necessary
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import filters
from dynamic_rest.viewsets import WithDynamicViewSetMixin
class CustomerHotelBookOrderList(WithDynamicViewSetMixin,ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = HotelPackageOrder.objects.all()
    serializer_class = CustomerOrderSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields =('process_state','closed','checkin_time')
    lookup_field = 'number'
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            print('to page')
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JSONWrappedResponse(serializer.data)

    @detail_route(methods=['GET','POST'], url_path='cancel')
    def handle_order(self, request, number=None, *args, **kwargs):
        """
        :param request:
        :param number: 订单号
        :return:
        """
        order = self.get_object()
        checker = ObjectPermissionChecker(request.user)
        # print(checker.has_perm('hotelpackageorder.change_process_state', order))
        #  用户取消订单
        success, order = order.customer_cancel_order(request.user)
        if (success):
            order.refresh_from_db()
        cs = CustomerOrderSerializer(order)
        return Response(wrapper_response_dict(message='退订成功', data={'order':cs.data}))





    def get_queryset(self,queryset=None):
        queryset = self.queryset
        user = self.request.user
        state = self.request.GET.get('state')
        return queryset.filter(customer=user)




# url is  order/customer
class CustomerOrderActionAPIView(WithDynamicViewSetMixin,ModelViewSet):
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
            success,order = request.order.customer_cancel_order(request.user)
            if(success):
                order.refresh_from_db()
            cs = CustomerOrderSerializer(hotelpackageorder)
            return Response(wrapper_response_dict(message='退订成功',data=cs.data))
        else:
            return Response(data='未知操作')


    def cancelBookOrder(self, request,):
        number = request.POST.get('number', None)
        order = HotelPackageOrder.objects.get(number=number)
        order.cancelBook(request.user)

class RoomPackageBookAPIView(APIView):
    """
    用户 订购 酒店
    权限：已登入用户
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # @transaction.atomic()
    @method_decorator(parameter_necessary('productId','checkinTime','checkoutTime','guests'))
    def post(self, request, *args, **kwargs):
        # 1 .商品是否存在
        # 2. 用户积分是否够
        # 3. 是否在区间存在已购订单
        # 3. 扣除积分，通知代理商

        user = request.user
        productId = kwargs.get('productId')
        checkinTime = kwargs.get('checkinTime')
        checkoutTime = kwargs.get('checkoutTime')
        checkinTime = datetime.strptime(checkinTime, '%Y-%m-%d').date()
        checkoutTime = datetime.strptime(checkoutTime, '%Y-%m-%d').date()
        guests = kwargs.get('guests')
        if(guests):
            print('guests is ')

        # check id 是否真实
        try:
            room_package = RoomPackage.objects.get(id=productId)

        except RoomPackage.DoesNotExist:
            return DefaultJsonResponse(message='不存在该商品', code=403)

        # check 在区间是否存在订单
        exist = HotelPackageOrder.objects.filter(customer=user,checkin_time__lte=checkinTime,checkout_time__gt=checkinTime).exists()
        if exist:
            return Response(wrapper_response_dict(code=-100,message='存在订单,请先取消'))
        # check 预订时间是否准确
        check_validate_checkTime(room_package,checkinTime,checkoutTime)
        # check point 是否足够
        request_notes = '需要wifi'
        hotelPackageOrder = generateHotelPackageProductOrder(request, user, room_package, request_notes, checkinTime,
                                                             checkoutTime)
        serializer = CustomerOrderSerializer(hotelPackageOrder)

        return DefaultJsonResponse(res_data=serializer.data,message='预订成功')


def check_point_enough_book(user, room_package, checkinTime, checkoutTime, ):
    daystates = room_package.roompackage_daystates.filter(date__gte=checkinTime,date__lt=checkoutTime,daystate=1)

    # todo 保证 state 为可预订状态

    sum_point = sum(daystate.need_point for daystate in daystates)
    if user.point >= sum_point:
        return True,sum_point
    else:
        return False



def generateHotelPackageProductOrder(request, member_user, room_package, request_notes, checkinTime, checkoutTime):
    days = (checkoutTime - checkinTime).days
    daystates = room_package.roomstates.filter(date__gte=checkinTime,date__lt=checkoutTime)
    # 保证 state 为可预订状态
    if (daystates.count() != days):
        raise ConditionDenied(detail='该套餐已满')
    sum_point = sum(daystate.need_point for daystate in daystates)

    try:
        with transaction.atomic():
            if member_user.point <= sum_point:
                raise PointNotEnough()
            sum_front_price = sum(daystate.front_price for daystate in daystates)
            print('sum points {}'.format(sum_point))
            print('sum_front_price {}'.format(sum_front_price))
            hotel_package_order = HotelPackageOrder(
                request_notes =request_notes,
                customer=member_user,
                seller=room_package.owner,
                product=room_package,
                checkin_time = checkinTime,
                checkout_time= checkoutTime,
                total_need_points = sum_point,
                total_front_prices = sum_front_price,
                breakfast = room_package.breakfast,
                hotel_name = room_package.hotel.name,
                room_name = room_package.room.name
            )
            try:
                order_numbers = HotelOrderNumberGenerator.objects.get(id="order_number")
            except HotelOrderNumberGenerator.DoesNotExist:
                order_numbers = HotelOrderNumberGenerator.objects.create(id="order_number")
            order_numbers.init(request,hotel_package_order)
            hotel_package_order.number = order_numbers.get_next()
            print('为number 赋值{}'.format(hotel_package_order.number))
            hotel_package_order.save()
            # new Order
            orderItems = []

            for daystate in daystates:
                item = HotelPackageOrderItem(
                    order=hotel_package_order,
                    product_name= '',
                    product_code=room_package.id,
                    product=room_package,
                    day= daystate.date,
                    point=daystate.need_point,
                    front_price=daystate.front_price,
                    )
                item.save()
                orderItems.append(item)
            # 扣除积分
            member_user.deductPoint(sum_point)
            member_user.save()
            # 配置权限
            assign_perm('change_process_state',member_user,hotel_package_order,)
            return hotel_package_order
    except Exception as e:
        raise e
        raise APIException(detail='服务器错误')



def add_hotel_order(request,member_user,product,request_notes,checkinTime,checkoutTime):
    hotelPackageOrder = generateHotelPackageProductOrder(request,member_user,product,request_notes,checkinTime,checkoutTime)
    # return DefaultJsonResponse(res_data='订购成功,id 是{0}'.format(hotelPackageOrder.order.number))
    serializer = CustomerOrderSerializer(hotelPackageOrder)
    return DefaultJsonResponse(res_data=serializer.data)

def check_validate_checkTime(product,checkinTime,checkoutTime):

    pass