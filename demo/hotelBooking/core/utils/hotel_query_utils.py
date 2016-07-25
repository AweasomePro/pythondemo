# import datetime
import datetime

from django.db.models import Count
from hotelBooking.models.products import RoomDayState


def query(queryset,cityId,checkinTime,checkoutTime):
    cityId = int(cityId)
    checkin_time = datetime.datetime.strptime(checkinTime, '%Y-%m-%d').date()
    checkout_time = datetime.datetime.strptime(checkoutTime, '%Y-%m-%d').date()
    check_days = (checkout_time - checkin_time).days
    print(checkin_time)
    print(checkout_time)
    states = RoomDayState.objects.filter(city_id=cityId).values('roomPackage', 'hotel') \
        .filter(date__gte=checkin_time, date__lt=checkout_time,
                state=1).annotate(
        consecutive_days=Count('state')).filter(consecutive_days=(check_days )).distinct().order_by('hotel')
    # print(type(states))
    s = set()
    for i in states:
        s.add(i['hotel'])
    # print(s)
    queryset = queryset.filter(id__in=s)
    return queryset
