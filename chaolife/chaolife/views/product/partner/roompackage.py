# -*- coding:utf-8 -*-
from django.db import transaction
from django.utils.decorators import method_decorator
from dynamic_rest.filters import DynamicFilterBackend, DynamicSortingFilter
from rest_framework.decorators import detail_route,list_route
from rest_framework.filters import BaseFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from chaolife.models import Hotel
from chaolife.models.products import Product, RoomDayState
from chaolife.models.products import RoomPackage
from chaolife.serializers.products import PartnerRoomPackageSerializer
from chaolife.utils.AppJsonResponse import DefaultJsonResponse
from chaolife.exceptions import ConditionDenied, PermissionDenied
from common.utils.AppJsonResponse import DefaultJsonResponse
from chaolife.permissions.rolepermissions import IsHotelPartnerRole
from chaolife.permissions.productpermissions import IsProductOwner
from dynamic_rest.viewsets import DynamicModelViewSet
from chaolife.serializers.products import RoomDayStateSerializer
from common.viewsets import CustomSupportMixin
from common.decorators import parameter_necessary
from common.utils import requestutil,dateutils
from hotel.serializers.roomstates import UpdateSingleRoomDaystateSerializer


class CheckFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        Return a filtered queryset.
        """
        str_active = request.GET.get('active')
        if str_active == 'True':
            return queryset.filter(active=True)
        elif str_active == 'False':
            print(' you requets false')
            return queryset.filter(active= False)
        return queryset


class PartnerRoomPackageView(CustomSupportMixin,DynamicModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,IsHotelPartnerRole,IsProductOwner)
    serializer_class = PartnerRoomPackageSerializer
    queryset = RoomPackage.objects.all()
    filter_backends = (CheckFilterBackend,DynamicFilterBackend, DynamicSortingFilter)

    def retrieve(self, request, *args, **kwargs):
        # hotel_query_utils.query(1,0,0)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return DefaultJsonResponse(data=serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    #warn 不应该支持update

    @list_route(methods=['GET','PUT'], url_path='joined_hotel', )
    def get_joined_hotel(self,request,*args,**kwargs):
        res = self.queryset.values('hotel','hotel_name').order_by().distinct()
        print(res)
        return DefaultJsonResponse(message='success',data=res)

    @detail_route(methods=['GET','PUT'], url_path='delete', )
    def delete_product(self,request,*args,**kwargs):
        roomPackage = self.get_object()
        roomPackage.deleted = True
        roomPackage.checked = False
        roomPackage.active = False
        roomPackage.save(update_fields=('deleted','checked','active'))
        return DefaultJsonResponse(message='删除成功')

    @detail_route(methods=['GET','PUT'], url_path='active', )
    def active_product(self, request, *args, **kwargs):
        roomPackage = self.get_object()
        if roomPackage.room.checked == False:
            raise ConditionDenied('该房型暂未审核')
        roomPackage.set_active()
        roomPackage.save(update_fields=('active',))
        return DefaultJsonResponse(message='上线成功')

    @detail_route(methods=['GET','PUT' ], url_path='deactive', )
    def deactive_product(self, request, *args, **kwargs):
        roomPackage = self.get_object()
        roomPackage.active = False
        roomPackage.save(update_fields=('active',))
        return DefaultJsonResponse(message='下线成功')

    @list_route(methods=['PUT','POST'],url_path='active')
    def getDateRange(self,request):
        startDate,endDate = requestutil.getDateRange(request)
        pass


    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        from chaolife.serializers.products import RoomPackageCreateSerializer
        request_data = request.data.copy()
        if not request.user.is_partner_member:
            raise PermissionDenied()
        if (int(request.data.get('room')) == -1):  # 约定 -1表示 customRoomName字段有效 有效
            roomId = self.validate_custom_room_name(request.data.get('hotel'), request.data.get('customRoomName'))
            request_data['room'] = roomId
        request_data['owner'] = request.user.id
        print(request.user.id)
        s = RoomPackageCreateSerializer(data=request_data,context={'request':self.request})
        s.is_valid(raise_exception=True)
        s.save()
        return DefaultJsonResponse(message='创建成功审核中')

    def get_queryset(self, queryset=None):
        return self.queryset.filter(owner=self.request.user,deleted=False)

    @detail_route(methods=['POST'],url_path = 'modify/dayprice')
    def modifyDayPrice(self,request,pk):
        roomPackage = self.get_object()
        from hotel.serializers import UpdateRoomDayStatesSerializer
        data = request.data.copy()
        s = UpdateRoomDayStatesSerializer(data=data, roomPackage=self.get_object())
        s.is_valid(raise_exception=True)
        roomPackage = RoomPackage.objects.get(id=roomPackage.id)
        return DefaultJsonResponse(message='success，修改了{}条数据'.format(s.save()),
                                   data=self.serializer_class(roomPackage).data)

    @detail_route(methods=['POST', ], url_path='modify/daystates', )
    def modifyDayStates(self, request, pk):
        #兼容老接口
        return self.modifyDayPrice(request,pk)


    @detail_route(methods=['PUT','POST'],url_path='modify/daystate')
    def multi_modify_daystate(self,request,pk):
        if request.version == 0.1:
            print('跑到老接口去')
            return self.update_single_roomDaystate(request, pk)
        #新版本
        dates = request.data.getlist('date')
        print('dates is {}'.format(dates))
        state = request.data.get('state')
        count = RoomDayState.objects.filter(roomPackage=self.get_object(),date__in=dateutils.multi_formate_str_to_date(dates)).update(
            state = state
        )
        return DefaultJsonResponse(message='成功修改了{}'.format(count))

    @detail_route(methods=['POST', ], url_path='modify/daystate', )
    def update_single_roomDaystate(self, request, pk,):
        s = UpdateSingleRoomDaystateSerializer(data=request.data, roomPackage=self.get_object())
        s.is_valid(raise_exception=True)
        daystate = s.save()
        return DefaultJsonResponse(data= {'daystate':RoomDayStateSerializer(daystate).data})

    def validate_custom_room_name(self, hotelId, value):
        # todo 判断是否已经存在
        print('value is {}'.format(value))
        from chaolife.models import Room
        try:
            Hotel.objects.get(id=hotelId).hotel_rooms.get(name=value)
        except Room.DoesNotExist:
            from chaolife.models import Room
            room = Room(name=value, hotel_id=hotelId)
            room.save()
            return room.id
        except Room.MultipleObjectsReturned:
            raise ConditionDenied(detail='房型名已经存在')
            # warn this is should be excepted
        else:
            raise ConditionDenied(detail='房型名已经存在')


    def get_serializer_class(self):
        #    todo  通过判断请求方法 或者请求的地址提供不同的 serializser
        return self.serializer_class

