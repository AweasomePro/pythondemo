from django.db import transaction
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
from hotelBooking import Province,City,Hotel,House,User
from hotelBooking.core.models.user import CustomerMember,PartnerMember
from hotelBooking.module import sms,push
@api_view(['POST',])
def test(request,):
    print(request.POST)
    pushMessage()
    return Response('success')

@api_view(['POST',])
def testsms(request):
    response = sms.request_sms_code(phone_number='15726814574',template='login')
    return response
def createHousePackage():

    housepackage = HousePackage(owner=User.objects.first())
    housepackage.package_state = 1
    housepackage.house = House.objects.first()
    housepackage.front_price = 340
    housepackage.package_state = 1
    housepackage.save()
    house = housepackage.house
    hotel = house.hotel
    city = hotel.city
    if housepackage.housepackage_roomstates.all().count() == 0:
        roomstates = []
        # 说明是第一次创建
        print('len is 0 ,will auto create')
        day = datetime.datetime.today()
        house_type = housepackage.house
        owner = housepackage.owner
        for i in range(0, 30):
            print(day.strftime('%Y-%m-%d'))
            print(i)
            obj = AgentRoomTypeState(agent=owner,
                                     housePackage=housepackage,
                                     house_type=house_type,
                                     hotel=hotel,
                                     city=city,
                                     state=AgentRoomTypeState.ROOM_STATE_ENOUGH,
                                     date=day.strftime('%Y-%m-%d'))
            roomstates.append(obj)
            day += timedelta(days=1)
        AgentRoomTypeState.objects.bulk_create(roomstates)
    return Response('success')

def pushMessage():
    push.send(data={'alert':'diu 你老母'})

def initData():
    try:
        with transaction.atomic():
            p = Province(name='浙江',name_py='ZheJiang')
            p.save()
            city = City(name='宁波',name_py='NingBo',code=1234,province=p)
            city.save()
            hotel = Hotel(name='酒店名字',address='address',contact_phone=15726814574,introduce='一家酒店',city=city)
            hotel.save()
            house  = House(hotel=hotel,name='商务大床',)
            house.save()
            u = User()
            u.phone_number = 15726814574
            u.set_password(123456)
            u.save()
            c = CustomerMember(user =u)
            c.save()
            p = PartnerMember(user=u)
            p.save()
            hp = HousePackage(owner=u,house=house,need_point=20,front_price=130,detail='zao')
            hp.save()
            return Response({'res': 'success'})
    except BaseException:
        return Response('内部错误')
