# -*- coding:utf-8 -*-
from datetime import datetime

from django.db.models import Prefetch
from dynamic_rest.viewsets import DynamicModelViewSet, WithDynamicViewSetMixin
from rest_framework.viewsets import GenericViewSet

from rest_framework import generics, mixins, views,viewsets
from django.views.decorators.cache import cache_page
from rest_framework_extensions.cache.decorators import cache_response

from chaolife.core.utils import hotel_query_utils
from chaolife.models import RoomDayState
from chaolife.models import RoomPackage
from chaolife.models.hotel import Hotel
from chaolife.models.hotel import Room
from chaolife.pagination import StandardResultsSetPagination
from chaolife.serializers import RoomSerializer, HotelSerializer
from chaolife.serializers.hotels import HotelDetailSerializer
from chaolife.utils import dateutils
from chaolife.utils.AppJsonResponse import DefaultJsonResponse
from rest_framework_extensions.mixins import (
    ReadOnlyCacheResponseAndETAGMixin
)
from common.viewsets import CustomSupportMixin


class HotelViewSet(ReadOnlyCacheResponseAndETAGMixin,CustomSupportMixin,WithDynamicViewSetMixin,viewsets.ReadOnlyModelViewSet):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()
    pagination_class = StandardResultsSetPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print(serializer.data)
        return DefaultJsonResponse(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            print(request.query_params.get('checkinTime'))
            print('我们设置了checkinTime')
            checkinTime = self.request.query_params.get('checkinTime',None)
            context = {'request':self.request}
            if checkinTime:
                context['checkinTime'] = dateutils.formatStrToDate(checkinTime)
            serializer = HotelSerializer(
                page,
                many=True,
                context=context,
                sideload=True
            )
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return DefaultJsonResponse(serializer.data, code=100, message='成功')

    def get_queryset(self, queryset=None):
        if (queryset == None):
            queryset = self.queryset
        # 客户端查询
        cityId = self.request.query_params.get('cityId',None)
        checkinTime = self.request.query_params.get('checkinTime',None)
        checkoutTime = self.request.query_params.get('checkoutTime',None)
        if (checkinTime and checkoutTime and cityId): #todo 该方法效率不高
            queryset = hotel_query_utils.query(queryset, cityId, checkinTime, checkoutTime).\
                prefetch_related('hotel_rooms').prefetch_related(Prefetch('hotel_rooms__roomPackages',queryset=RoomPackage.objects.filter(checked=True,active=True,deleted=False)))
            return queryset
        if(cityId):
            queryset = queryset.filter(city__code=cityId)
            return queryset
        return queryset


class HotelDetialView(CustomSupportMixin,WithDynamicViewSetMixin,mixins.RetrieveModelMixin,
                           GenericViewSet):

    queryset = Hotel.objects.get_queryset()
    serializer_class = HotelDetailSerializer


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance,context={'request':request},exclude_fields =('city','agent'))
        return DefaultJsonResponse(serializer.data)


    def get_queryset(self,queryset=None):
        request = self.request
        checkinTime = request.GET.get('checkinTime', None)
        checkoutTime = request.GET.get('checkoutTime', None)
        queryset = self.queryset\
            .prefetch_related(Prefetch('hotel_rooms',queryset=Room.objects.filter(checked=True,active=True)))\
            .prefetch_related('hotel_rooms__room_imgs')\
            .prefetch_related(Prefetch('hotel_rooms__roomPackages',queryset=RoomPackage.objects.filter(checked=True,active=True,deleted=False)))
        # 如果带了check time 则只返回 那区间的 roomdaystate
        if(checkinTime and checkoutTime):
            filter_date_queryset = queryset.prefetch_related(Prefetch('hotel_rooms__roomPackages__roomstates',
                                                                      queryset=RoomDayState.objects.filter(date__gte=dateutils.formatStrToDate(checkinTime),
                                                                                                           date__lt = dateutils.formatStrToDate(checkoutTime))))
            return filter_date_queryset
        else:
            filter_date_queryset = queryset.prefetch_related(Prefetch('hotel_rooms__roomPackages__roomstates',
                                                                       queryset=RoomDayState.objects.filter(date__gte=dateutils.today())))
            return filter_date_queryset


class RoomViewSet(DynamicModelViewSet):

    serializer_class = RoomSerializer
    queryset = Room.objects.all().filter(checked=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance,)
        return DefaultJsonResponse(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data =  self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return DefaultJsonResponse(data=serializer.data)

    def get_serializer(self, *args, **kwargs):
        return super(
            DynamicModelViewSet, self).get_serializer(
            *args, **kwargs)

# todo 根据酒店id   返回 该酒店目前支持的房型

class RoomTypesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    获得某酒店的所有房型名称
    """
    pagination_class = StandardResultsSetPagination
    serializer_class = RoomSerializer

    def list(self, request, hotel_pk = None,*args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(hotel_id=hotel_pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'roomtypes':serializer.data})
        serializer = self.get_serializer(queryset, many=True)
        return DefaultJsonResponse({'roomtypes':serializer.data})


    def get_queryset(self):
         return Room.objects.all().filter(checked=True)

    def get_serializer_class(self,*args,**kwargs):
        return RoomSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(exclude_fields=('roomPackages','room_imgs',),*args, **kwargs)

