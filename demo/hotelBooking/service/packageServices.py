from hotelBooking.models.products import RoomPackage,RoomDayState
from datetime import datetime, timedelta


def createRoomDaysetsFormRoomPackage(roomPackage):
    roomstates = []
    day = datetime.today().date()
    assert day == roomPackage.created_on.date()
    for i in range(0, 30):
        print(day.strftime('%Y-%m-%d'))
        print(i)
        obj = RoomDayState(agent=roomPackage.owner,
                           roomPackage=roomPackage,
                           room=roomPackage.room,
                           hotel=roomPackage.hotel,
                           city=roomPackage.hotel.city,
                           need_point=roomPackage.default_point,
                           front_price=roomPackage.default_front_price,
                           state=RoomDayState.ROOM_STATE_ENOUGH,
                           date=day.strftime('%Y-%m-%d')
                           )
        roomstates.append(obj)
        day += timedelta(days=1)
    RoomDayState.objects.bulk_create(roomstates)