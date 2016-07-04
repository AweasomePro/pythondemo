import datetime
now = datetime.datetime.now()
# str =datetime.datetime.now().strftime('%Y%m%d%H')[2:]
# print(str)
import django.utils.timezone
from django.utils.timezone import datetime
from django.utils.dates import WEEKDAYS
now = datetime.now()
print(type(now))
print(now.day)
print(datetime.now().replace(day=datetime.now().day+1).strftime('%Y-%m-%d'))
# datetime.date().today()