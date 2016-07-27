from hotelBooking.models import HotelPackageOrder
from hotelBooking.models.products import RoomPackage,RoomDayState
from datetime import datetime, timedelta


def createRoomDaysFormRoomPackage(roomPackage):
    """
    创建 对应roompackage 的 30天周期房态
    这个方法方法在celery中调用
    :param roomPackage:
    :return:
    """
    roomStates = []
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
        roomStates.append(obj)
        day += timedelta(days=1)
    RoomDayState.objects.bulk_create(roomStates)

def exit_sameday_order(user,checkin_date):
    return HotelPackageOrder.objects.filter(customer=user, checkin_time__lte=checkin_date,
                                     checkout_time__gt=checkin_date).exists()