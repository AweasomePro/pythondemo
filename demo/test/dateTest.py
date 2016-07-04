import datetime
now = datetime.datetime.now()
str =datetime.datetime.now().strftime('%Y%m%d%H')[2:]
print(str)
import django.utils.timezone
from django.utils.timezone import datetime
print(datetime.now())
print()
# d = datetime.datetime.strptime(str(now), '%Y-%m-%d %H:%M:%S')