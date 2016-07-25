from django.db import transaction

from hotelBooking.exceptions import PointNotEnough, ConditionDenied
from hotelBooking.models.orders import HotelPackageOrder, HotelPackageOrderItem
from hotelBooking.models.plugins import HotelOrderNumberGenerator
from hotelBooking.serializers import CustomerOrderSerializer
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse


def verifyPointEnough(customer, hotelPackageProduct):
    if customer.user.point <= hotelPackageProduct.need_point:
        raise PointNotEnough(detail='购买该套餐个所需积分不够')


def get_customer_member_object( request):
    if not request.user.is_customer_member:
        return DefaultJsonResponse(res_data='你还不是会员', code=-100)
    return request.user

def is_hotel_package(product):
    # return product.name == '酒店套餐'
    # todo 判断类型
    return True


def generateHotelPackageProductOrder(request, member_user, room_package, request_notes, checkinTime, checkoutTime):
    days = (checkoutTime - checkinTime).days
    daystates = room_package.roomstates.filter(date__gte=checkinTime,date__lt=checkoutTime)
    # 保证 state 为可预订状态
    if (daystates.count() != days):
        raise ConditionDenied(detail='该套餐已满')
    sum_point = sum(daystate.need_point for daystate in daystates)
    if(member_user.point < sum_point):
        raise PointNotEnough()
    try:
        with transaction.atomic():
            if member_user.point <= sum_point:
                raise PointNotEnough()
            # 合计前台付款
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
            print('生成订单号{}'.format(hotel_package_order.number))
            hotel_package_order.save()
            # new Order
            orderItems = []
            assert daystates != None
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
            # todo 这些操作可以加入 异步队列中
            # assign_perm('change_process_state',member_user,hotel_package_order,)
            return hotel_package_order
    except Exception as e:
        raise e



def add_hotel_order(request,member_user,product,request_notes,checkinTime,checkoutTime):

    hotelPackageOrder = generateHotelPackageProductOrder(request,member_user,product,request_notes,checkinTime,checkoutTime)
    # return DefaultJsonResponse(res_data='订购成功,id 是{0}'.format(hotelPackageOrder.order.number))
    serializer = CustomerOrderSerializer(hotelPackageOrder)

    return DefaultJsonResponse(res_data=serializer.data)




