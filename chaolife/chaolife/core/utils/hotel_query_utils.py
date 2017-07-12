#-*- coding: utf-8 -*-
# import datetime
import datetime

from django.db.models import Count
from django.db.models import Prefetch

from chaolife.models import Hotel
from chaolife.models.products import RoomDayState,RoomPackage,Room


def query(queryset,cityId,checkinTime,checkoutTime):
    checkin_time = datetime.datetime.strptime(checkinTime, '%Y-%m-%d').date()
    checkout_time = datetime.datetime.strptime(checkoutTime, '%Y-%m-%d').date()
    check_days = (checkout_time - checkin_time).days
    roomIdSet = Room.objects.filter(checked=True,active=True,deleted=False,).values('id')
    print(roomIdSet)
    roomPackage = RoomPackage.objects.select_related('room').filter(active=True,deleted=False,checked=True,room_id__in =roomIdSet).prefetch_related(Prefetch('roomstates',queryset=RoomDayState.objects.filter(date__gte=checkin_time, date__lt=checkout_time,
                state=1)),).filter(city_id=cityId).all().values('id')

    print('打印roomPackage{}'.format(roomPackage))
    states = RoomDayState.objects.filter(roomPackage_id__in=roomPackage).values('roomPackage', 'hotel') \
        .filter(date__gte=checkin_time, date__lt=checkout_time,
                state=1).annotate(
        consecutive_days=Count('state')).filter(consecutive_days=(check_days)).distinct().order_by('hotel')
    s = set()
    for i in states:
        s.add(i['hotel'])
    queryset = queryset.filter(city_id=cityId, id__in=s)
    return queryset
     # ---------------------------- Not Work ________________________________________________________________
    # hotels = Hotel.objects.filter(city_id=cityId).prefetch_related(
    #     Prefetch('hotel_rooms',
    #              queryset=Room.objects.filter(active=True).prefetch_related(
    #                  Prefetch('roomPackages',
    #                           queryset=RoomPackage.objects.filter(active=True).prefetch_related(
    #                               Prefetch('roomstates',queryset=RoomDayState.objects.filter(date__gte=checkin_time, date__lt=checkout_time,state=1).annotate(
    #     consecutive_days=Count('state')).filter(consecutive_days=(check_days)).distinct(),to_attr='some_roomPackages'
    #                                        )
    #                           )
    #                     )
    #              ).annotate(count_roompackages = Count('roomPackages')).filter(count_roompackages__gt=0),to_attr='rooms'
    #         )
    # ).annotate(count_rooms = Count('hotel_rooms'),).filter(count_rooms__gt=0).all()
    # print(hotels)
    # for hotel in hotels:
    #     for room in hotel.rooms:
    #         print('rootpackages = {}'.format(room.count_roompackages))
    #         for roomPackage in room.some_roomPackages:
    #             print(roomPackage)
    #     print(hotel.count_rooms)
    #     print(hotel.roompackage_set)

