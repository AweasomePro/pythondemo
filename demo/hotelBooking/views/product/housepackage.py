from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.datetime_safe import datetime
from django.views.generic import ListView
from dynamic_rest.viewsets import DynamicModelViewSet
from hotelBooking.utils.decorators import parameter_necessary
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
from hotelBooking.auth.decorators import login_required_and_is_member, login_required_and_is_partner
from hotelBooking.core.serializers.products import RoomTypeStateSerializer, HousePackageSerializer
from hotelBooking.core.utils import hotel_query_utils
from hotelBooking.core.utils.serializer_helpers import wrapper_response_dict
from hotelBooking.test.performance import fn_time
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse
from hotelBooking.core.models.orders import HotelPackageOrder,HotelPackageOrderSnapShot
# from hotelBooking import RoomType
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


"""
@api {post} /product/hoousepackage/?action=create
@apiName create new hotel package
@apiGroup partner 合作商户
@apiParam {hotelid} id of hte hotel model primary key.
@apiParm {frontPrice} front desk price
@apiParm {point}  need deducted the point
@apiParm {housetype} the room type like '豪华双床房'
@apiSuccess {String} firstname Firstname of the User.
@apiSuccess {String} lastname  Lastname of the User.
"""
@api_view(['POST',])
@parameter_necessary('hotelId', 'point', 'price', 'breakfast', optional=('customHouseTypeName','houseId'))
@login_required_and_is_partner()
@authentication_classes([JSONWebTokenAuthentication])
def create_new_hotelpackage(request,hotelId,point,price,breakfast,customHouseTypeName,houseId,*args, **kwargs):
    # 注意 atomic 需要有捕获异常，如果你内部catch 了，等于失效了
    # 前端需要注意，进行 customHouseTypeName 是否已存在的判断，所有的最终都是需要服务端审核的
    # print(hotelId)
    # print(houseId)
    # print(point)
    # print(price)
    # print(breakfast)
    # print(request.user)
    NONE_HOUSE = -1
    h = houseId
    print('houseId is {}'.format(houseId))
    # assert not (customHouseTypeName is None and houseId is -1)
    try:
        with transaction.atomic():
            if (int(houseId) == NONE_HOUSE):
                house = House(hotel_id=hotelId,name=customHouseTypeName)
                house.save()
                houseId = house.id
            housepackage = HousePackage(
                house_id = houseId,
                owner=request.user,
                need_point = point,
                front_price = price,
                breakfast = breakfast,
            )
            housepackage.save()
            return Response(wrapper_response_dict(message='创建成功审核中'))
    except Exception as e:
        print(e.__cause__)
        return Response(wrapper_response_dict(message='失败，服务器异常,需上报并记录',code=-100))



    #
    #
    # housepackage = HousePackage(owner=User.objects.first())
    # pararms = request.POST
    #
    # housepackage.package_state = 1
    # housepackage.house = House.objects.first()
    # housepackage.front_price = 340
    # housepackage.package_state = 1
    # housepackage.save()
    # house = housepackage.house
    # hotel = house.hotel
    # city = hotel.city
    # if housepackage.housepackage_roomstates.all().count() == 0:
    #     roomstates = []
    #     # 说明是第一次创建
    #     print('len is 0 ,will auto create')
    #     day = datetime.today().date()
    #     house_type = housepackage.house
    #     owner = housepackage.owner
    #     for i in range(0, 30):
    #         print(day.strftime('%Y-%m-%d'))
    #         print(i)
    #         obj = AgentRoomTypeState(agent=owner,
    #                                  housePackage=housepackage,
    #                                  house_type=house_type,
    #                                  hotel=hotel,
    #                                  city=city,
    #                                  state=AgentRoomTypeState.ROOM_STATE_ENOUGH,
    #                                  date=day.strftime('%Y-%m-%d'))
    #         roomstates.append(obj)
    #         day += timedelta(days=1)
    #     AgentRoomTypeState.objects.bulk_create(roomstates)
    # return Response(wrapper_response_dict(message='创建成功,审核中'))






class HousePackageStateView(DynamicModelViewSet):
    serializer_class = RoomTypeStateSerializer
    queryset = AgentRoomTypeState.objects.all()
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(wrapper_response_dict(serializer.data))
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



class HousePackageView(DynamicModelViewSet):
    serializer_class = HousePackageSerializer
    queryset = HousePackage.objects.all()

    def retrieve(self, request, *args, **kwargs):
        print('do retreieve')
        # hotel_query_utils.query(1,0,0)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print('will be serializer')
        return Response(wrapper_response_dict(data=serializer.data))
        # return Response('success')

# todo 不适合放在这个包下
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





