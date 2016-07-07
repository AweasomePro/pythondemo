from rest_framework.decorators import api_view
from rest_framework.response import Response

from hotelBooking import Product,HousePackage
from hotelBooking import User
from django.utils.timezone import datetime
from django.utils.timezone import timedelta

from hotelBooking.core.models.products import AgentRoomTypeState


@api_view()
def test(request):
    p = Product()
    p.owner = User.objects.first()
    p.save()
    h = HousePackage()
    h.product = p
    h.package_state = 1
    h.house_id = 1
    h.front_price = 340
    h.package_state =1
    h.save()
    if h.agentroomtypestate_set.all().count() == 0:
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

            obj = AgentRoomTypeState( agent=owner,
                housePackage=housePackage,
                house_type=house_type,
                state=AgentRoomTypeState.ROOM_STATE_ENOUGH,
                date=day.strftime('%Y-%m-%d'))
            roomstates.append(obj)
            day += timedelta(days=1)
        AgentRoomTypeState.objects.bulk_create(roomstates)
    return Response({'res':'success'})