from datetime import timedelta

from django.utils.timezone import datetime

from django.db import transaction
from hotelBooking.models import RoomPackage,RoomDayState,Hotel,TestModel
class RoomPackageCreator(object):

    def createRoomPackage(self, owner, hotel, room, default_point, default_price, breakfast):
        # owner = partner, room = room, hotel = hotel, default_point = 20, default_front_price = 130, detail = 'zao'
        try:
            with transaction.atomic():
                roompackage = RoomPackage.objects.create(
                    owner = owner,
                    hotel = hotel,
                    room =room,
                    default_point = default_point,
                    default_front_price = default_price,
                    breakfast = breakfast
                )
                # 说明是第一次创建
                # print('len is 0 ,will auto create')
                # day = datetime.today()
                # city =hotel.city
                # roomstates = []
                # for i in range(0, 30):
                #     print(day.strftime('%Y-%m-%d'))
                #     print(i)
                #     obj = RoomDayState(agent=owner,
                #                        roomPackage=roompackage,
                #                        room=room,
                #                        hotel=hotel,
                #                        city=city,
                #                        need_point=default_point,
                #                        front_price= default_price,
                #                        state=RoomDayState.ROOM_STATE_ENOUGH,
                #                        date=day.strftime('%Y-%m-%d')
                #                        )
                #
                #     roomstates.append(obj)
                #     day += timedelta(days=1)
                # RoomDayState.objects.bulk_create(roomstates)
                roompackage.save()
                print('创建了roompackage')
                return roompackage
        except Hotel.DoesNotExist as e:
            print('error hotel id')
            raise e

    def createRoomDayState(self):
        pass