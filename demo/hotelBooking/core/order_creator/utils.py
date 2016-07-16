from guardian.shortcuts import assign_perm
from hotelBooking.core.exceptions import PointNotEnough
from hotelBooking.models.orders import HotelPackageOrder
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


def generateHotelPackageProductOrder(request,member_user,product,request_notes,checkinTime,checkoutTime):

    hotel_package_order = HotelPackageOrder.objects.create(
        request_notes =request_notes,
        customer=member_user,
        seller=product.owner,
        product=product,
        checkin_time = checkinTime,
        checkout_time= checkoutTime
    )
    hotel_package_order.save()

    try:
        order_numbers = HotelOrderNumberGenerator.objects.get(id="order_number")
    except HotelOrderNumberGenerator.DoesNotExist:
        order_numbers = HotelOrderNumberGenerator.objects.create(id="order_number")
    # new Order
    order_numbers.init(request,hotel_package_order)

    hotel_package_order.number = order_numbers.get_next()

    hotel_package_order.save()
    member_user.deductPoint(product.need_point)
    member_user.save()
    # 配置权限
    assign_perm('change_process_state',member_user,hotel_package_order,)
    return hotel_package_order

def add_hotel_order(request,member_user,product,request_notes,checkinTime,checkoutTime):

    hotelPackageOrder = generateHotelPackageProductOrder(request,member_user,product,request_notes,checkinTime,checkoutTime)
    # return DefaultJsonResponse(res_data='订购成功,id 是{0}'.format(hotelPackageOrder.order.number))
    serializer = CustomerOrderSerializer(hotelPackageOrder)

    return DefaultJsonResponse(res_data=serializer.data)




