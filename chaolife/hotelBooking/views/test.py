import datetime

from django.db import transaction
from django.utils.timezone import timedelta
from hotelBooking.models.province import Province
from hotelBooking.models.city import City
from hotelBooking.models.hotel import Hotel,Room
from hotelBooking.models.products import RoomPackage, RoomDayState
from hotelBooking.models import User
from hotelBooking.models.user import CustomerMember, PartnerMember
from hotelBooking.module import sms,push
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST',])
def test(request,):
    print(request.POST)
    initData()
    createRoomPackageState()
    return Response('success')

@api_view(['POST',])
def testsms(request):
    response = sms.request_sms_code(phone_number='15726814574',template='login')
    return response

@api_view(['GET',])
def init(request):
    initData()
    return Response('success')

def createRoomPackageState(roomPackage):
    room = roomPackage.room
    hotel = room.hotel
    city = hotel.city
    if roomPackage.roompackage_daystates.all().count() == 0:
        roomstates = []
        # 说明是第一次创建
        print('len is 0 ,will auto create')
        day = datetime.datetime.today()
        room = roomPackage.room
        owner = roomPackage.owner
        for i in range(0, 30):
            print(day.strftime('%Y-%m-%d'))
            print(i)
            obj = RoomDayState(agent=owner,
                               roomPackage=roomPackage,
                               room=room,
                               hotel=hotel,
                               city=city,
                               state=RoomDayState.ROOM_STATE_ENOUGH,
                               date=day.strftime('%Y-%m-%d')
                               )
            roomstates.append(obj)
            day += timedelta(days=1)
        RoomDayState.objects.bulk_create(roomstates)


def pushMessage():
    push.send(data={'alert':'diu 你老母'})


def initData():
    try:
        with transaction.atomic():
            partner_member = Province(name='浙江',)
            partner_member.save()
            city = City(name='宁波',code=1234,province=partner_member)
            city.save()
            hotel = Hotel(name='无敌酒店',address='address',contact_phone='15726814500',introduce='一家酒店',city=city)
            hotel.save()
            room  = Room(hotel=hotel, name='商务爆炸大床',checked=True,active=True )
            room.save()
            u = User.objects.create_user('15726814500',password=123456)
            u.save()
            c = CustomerMember(user =u)
            c.save()
            partner =  User.objects.create_user('15726814501',password=123456)
            partner_member = PartnerMember(user=partner)
            partner_member.save()
            # roompackage = RoomPackage(owner=partner, room=room,hotel=hotel, default_point=20, default_front_price=130, detail='zao')
            # roompackage.save()
            # createRoomPackageState(roompackage)
            return Response({'res': 'success'})
    except BaseException as e:
        raise e
