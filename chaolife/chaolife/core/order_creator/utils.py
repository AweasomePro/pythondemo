#-*- coding: utf-8 -*-
from django.db import transaction

from chaolife.exceptions import PointNotEnough, ConditionDenied
from chaolife.models.orders import HotelPackageOrder, HotelPackageOrderItem
from chaolife.models.plugins import HotelOrderNumberGenerator
from chaolife.serializers import HotelOrderSerializer
from chaolife.utils.AppJsonResponse import DefaultJsonResponse
from chaolife.tasks import createRoomDaysetsFormRoomPackage
from order.models import HotelOrderOptLog

def verifyPointEnough(customer, hotelPackageProduct):
    if customer.user.point <= hotelPackageProduct.need_point:
        raise PointNotEnough(detail='购买该套餐个所需积分不够')

def get_customer_member_object( request):
    if not request.user.is_customer_member:
        return DefaultJsonResponse(data='你还不是会员', code=-100)
    return request.user

def is_hotel_package(product):
    # return product.name == '酒店套餐'
    # todo 判断类型
    return True

def generateHotelPackageProductOrder(request, user, room_package, request_remark, checkinTime, checkoutTime, latest_checkin_hour, guests,price_type):
    # days = (checkoutTime - checkinTime).days
    # daystates = room_package.roomstates.filter(date__gte=checkinTime,date__lt=checkoutTime)
    # 保证 state 为可预订状态
    # if (daystates.count() != days):
    #     raise ConditionDenied(detail='该套餐已满')
    # if price_type ==1 :
    #     sum_point = sum(daystate.s_point for daystate in daystates)
    #     sum_price = sum(daystate.s_price for daystate in daystates)
    # else:
    #     sum_point = sum(daystate.d_point for daystate in daystates)
    #     sum_price = sum(daystate.d_price for daystate in daystates)
    # if(user.point < sum_point):
    #     raise PointNotEnough()
    # try:
    #     with transaction.atomic():
    #         hotel_package_order = HotelPackageOrder(
    #             request_remark =request_remark,
    #             customer=user,
    #             seller=room_package.owner,
    #             product=room_package,
    #             checkin_time = checkinTime,
    #             checkout_time= checkoutTime,
    #             latest_checkin_hour=latest_checkin_hour,
    #             total_need_points = sum_point,
    #             total_front_prices = sum_price,
    #             breakfast = room_package.breakfast,
    #             hotel_name = room_package.hotel.name,
    #             hotel_address=room_package.hotel.address,
    #             room_name = room_package.room.name,
    #             guests = guests,
    #             number=HotelOrderNumberGenerator.get_next_hotel_package_order_number(request)
    #         )
    #         hotel_package_order.save()
    #         # new Order
    #         orderItems = []
    #         for daystate in daystates:
    #             item = HotelPackageOrderItem(
    #                 order=hotel_package_order,
    #                 product_name= '',
    #                 product_code=room_package.id,
    #                 product=room_package,
    #                 day= daystate.date,
    #                 point=daystate.s_point,
    #                 price=daystate.s_price,
    #                 )
    #             item.save()
    #             orderItems.append(item)
    #         # 扣除积分
    #         user.deductPoint(sum_point)
    #         user.save()
    #         return hotel_package_order
    # except Exception as e:
    #     raise e
    pass






