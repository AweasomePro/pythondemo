from .common import *

DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hotel_book',  # 你的数据库名称
        'USER': 'zhuoxiuwu',  # 你的数据库用户名
        'PASSWORD': 'Zhuo8995588',  # 你的数据库密码
        'HOST': 'rm-bp13c9g5jzm1vpg51o.mysql.rds.aliyuncs.com',  # 你的数据库主机，留空默认为localhost
        'PORT': '3306',  # 你的数据库端口
    },
}
