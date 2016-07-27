
import datetime
from datetime import timedelta
in_str = '2016-07-07'
out_str = '2016-07-08'
in_array = in_str.split('-')
out_array = out_str.split('-')
checkin_time = datetime.datetime(int(in_array[0]),int(in_array[1]),int(in_array[2])).date()
checkout_time = datetime.datetime(int(out_array[0]),int(out_array[1]),int(out_array[2])).date()
interval =  (checkout_time-checkin_time).days
aDay = timedelta(days=1)

for i in range(1,interval+1):
    checkin_time += aDay
    print(checkin_time.day)


# str =datetime.datetime.now().strftime('%Y%m%d%H')[2:]
# print(str)
# import django.utils.timezone

# from django.utils.dates import WEEKDAYS
# now = datetime.now()
# print(now)
# print(type(now))
# print(now.day)
#
# print(datetime.today())
# print(datetime.now().replace(day=datetime.now().day).strftime('%Y-%m-%d'))
# datetime.date().today()
# today = datetime.today()
# day = datetime.today()
# for i in range(0,30):
#     print(day.strftime('%Y-%m-%d'))
#     print(i)
#     day +=timedelta(days=1)

