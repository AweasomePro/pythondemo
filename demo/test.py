import re
str = 'avatar_1000.png'
res =re.match('^avatar_(?P<id>\d+).png',str)
print(res.group('id'))
