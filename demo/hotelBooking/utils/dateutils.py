from datetime import datetime as real_datetime
from django.utils.datetime_safe import datetime


def caculatedays(startday,endday):

    checkin_time = real_datetime.strptime(startday, '%Y-%m-%d').date()
    checkout_time = real_datetime.strptime(endday, '%Y-%m-%d').date()
    return (checkout_time - checkin_time).days