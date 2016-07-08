from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hotelBooking import Product,HousePackage
from hotelBooking import User
import datetime
from django.utils.timezone import timedelta

from hotelBooking.core.models.products import AgentRoomTypeState

from hotelBooking import Hotel,House,HousePackage
from hotelBooking.core.models.products import Product,AgentRoomTypeState
@api_view(['POST',])
def test(request,):
    print(request.POST)
    # # createHousePackage()
    # in_str = '2016-07-07'
    # out_str = '2016-07-08'
    # checkin_time =     datetime.datetime.strptime(in_str,'%Y-%m-%d').date()
    # checkout_time = datetime.datetime.strptime(out_str,'%Y-%m-%d').date()
    # check_days = (checkout_time-checkin_time).days
    # print(checkin_time)
    # print(checkout_time)
    # states = AgentRoomTypeState.objects.filter(city_id=1).values('housePackage_id','hotel__id')\
    # .filter(date__gte=checkin_time, date__lte=checkout_time,
    #         state=1) \
    #     .annotate(
    #     consecutive_days=Count('state')
    # ).filter(consecutive_days=(check_days+1)).distinct().order_by('hotel')
    # print(type(states))
    # s = set()
    # for i in states:
    #     s.add(i['hotel__id'])
    # print(s)
    # hotels = Hotel.objects.filter(id__in=s)
    # print(hotels)

    return Response({'res':'success'})


def createHousePackage():
    p = Product()
    p.owner = User.objects.first()
    p.save()
    h = HousePackage()
    h.product = p
    h.package_state = 1
    h.house_id = 1
    h.front_price = 340
    h.package_state = 1
    h.save()
    house = h.house
    hotel = house.hotel
    city = hotel.city
    if h.housepackage_roomstates.all().count() == 0:
        roomstates = []
        # 说明是第一次创建
        print('len is 0 ,will auto create')
        day = datetime.today()
        housePackage = h.product.housepackage
        house_type = h.product.housepackage.house
        owner = h.product.owner
        for i in range(0, 30):
            print(day.strftime('%Y-%m-%d'))
            print(i)
            obj = AgentRoomTypeState(agent=owner,
                                     housePackage=housePackage,
                                     house_type=house_type,
                                     hotel=hotel,
                                     city=city,
                                     state=AgentRoomTypeState.ROOM_STATE_ENOUGH,
                                     date=day.strftime('%Y-%m-%d'))
            roomstates.append(obj)
            day += timedelta(days=1)
        AgentRoomTypeState.objects.bulk_create(roomstates)