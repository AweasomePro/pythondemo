import re
h_c = re.compile(pattern='(\d{2}):00')
res = h_c.match('12:00')
print(res.group())
print(res.groups()[0])
# a,b = res.group()
