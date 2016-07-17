from django.db import transaction
from dynamic_rest.viewsets import DynamicModelViewSet
from hotelBooking.auth.decorators import login_required_and_is_partner
from hotelBooking.core.order_creator.utils import add_hotel_order
from hotelBooking.core.utils.serializer_helpers import wrapper_response_dict
from hotelBooking.models import User,Hotel,Room
from hotelBooking.models.products import Product, RoomDayState
from hotelBooking.models.products import RoomPackage
from hotelBooking.models.ProductUtils import RoomPackageCreator
from hotelBooking.serializers.products import RoomDayStateSerializer, RoomPackageSerializer
from hotelBooking.utils.decorators import parameter_necessary
from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# from hotelBooking import Room
class HousePackageViewSet(viewsets.GenericViewSet):
    serializer_class = RoomPackageSerializer
    queryset = RoomPackage.objects.all()


class AddHousePackageView(APIView):

    def post(self, request, *args, **kwargs):
        user = User.objects.get(phone_number=15726814574)
        p = Product(owner=user)
        p.save()
        hp = RoomPackage(front_price=300, need_point=10, room=Room.objects.first(), product=p)
        hp.save()
        return Response(wrapper_response_dict(message='创建成功'))


"""
@api {post} /product/hoousepackage/?action=create
@apiName create new hotel package
@apiGroup partner 合作商户
@apiParam {hotelid} id of hte hotel model primary key.
@apiParm {frontPrice} front desk price
@apiParm {point}  need deducted the point
@apiParm {room} the room type like '豪华双床房'
@apiSuccess {String} firstname Firstname of the User.
@apiSuccess {String} lastname  Lastname of the User.
"""
@api_view(['POST',])
@parameter_necessary('hotelId', 'defaultPoint', 'defaultPrice', 'breakfast','roomId', optional=('customRoomName',))
@login_required_and_is_partner()
@authentication_classes([JSONWebTokenAuthentication])
def create_new_hotelpackage(request, hotelId, defaultPoint, defaultPrice, breakfast, customRoomName, roomId, *args, **kwargs):
    # 注意 atomic 需要有捕获异常，如果你内部catch 了，等于失效了
    # 前端需要注意，进行 customRoomName 是否已存在的判断，所有的最终都是需要服务端审核的

    NONE_ROOM = -1
    print('roomId is {}'.format(roomId))
    # assert not (customRoomName is None and roomId is -1)
    try:
        with transaction.atomic():
            if (int(roomId) == NONE_ROOM):
                room = Room(hotel_id=hotelId, name=customRoomName)
                room.save()
                roomId = room.id

            creater = RoomPackageCreator()
            package = creater.createRoomPackage(
                owner=request.user,
                hotel=Hotel.objects.get(id=hotelId),
                room= Room.objects.get(id=roomId),
                default_point = defaultPoint,
                default_price =defaultPrice,
                breakfast = breakfast
            )
            return Response(wrapper_response_dict(message='创建成功审核中'))
    except Exception as e:
        print(e.__cause__)
        raise e
        return Response(wrapper_response_dict(message='失败，服务器异常,需上报并记录',code=-100))



    #
    #
    # roompackage = RoomPackage(owner=User.objects.first())
    # pararms = request.POST
    #
    # roompackage.package_state = 1
    # roompackage.room = Room.objects.first()
    # roompackage.default_front_price = 340
    # roompackage.package_state = 1
    # roompackage.save()
    # room = roompackage.room
    # hotel = room.hotel
    # city = hotel.city
    # if roompackage.roompackage_roomstates.all().count() == 0:
    #     roomstates = []
    #     # 说明是第一次创建
    #     print('len is 0 ,will auto create')
    #     day = datetime.today().date()
    #     room = roompackage.room
    #     owner = roompackage.owner
    #     for i in range(0, 30):
    #         print(day.strftime('%Y-%m-%d'))
    #         print(i)
    #         obj = RoomDayState(agent=owner,
    #                                  roomPackage=roompackage,
    #                                  room=room,
    #                                  hotel=hotel,
    #                                  city=city,
    #                                  state=RoomDayState.ROOM_STATE_ENOUGH,
    #                                  date=day.strftime('%Y-%m-%d'))
    #         roomstates.append(obj)
    #         day += timedelta(days=1)
    #     RoomDayState.objects.bulk_create(roomstates)
    # return Response(wrapper_response_dict(message='创建成功,审核中'))






class HousePackageStateView(DynamicModelViewSet):
    serializer_class = RoomDayStateSerializer
    queryset = RoomDayState.objects.all()
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
    serializer_class = RoomPackageSerializer
    queryset = RoomPackage.objects.all()

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





