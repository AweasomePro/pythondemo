import datetime
now = datetime.datetime.now()
str =datetime.datetime.now().strftime('%Y%m%d%H')[2:]
print(str)
# d = datetime.datetime.strptime(str(now), '%Y-%m-%d %H:%M:%S')