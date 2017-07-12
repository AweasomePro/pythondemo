BROKER_URL = 'redis://redis-test.t0.daoapp.io:61107/0'
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chaolife',  # 你的数据库名称
        'USER': 'zhuoxiuwu',  # 你的数据库用户名
        'PASSWORD': 'Zhuo8995588',  # 你的数据库密码
        'HOST': 'rm-bp13c9g5jzm1vpg51o.mysql.rds.aliyuncs.com',  # 你的数据库主机，留空默认为localhost
        'PORT': '3306',  # 你的数据库端口
    },
}

import sys
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chaolife_test',  # 你的数据库名称
        'USER': 'root',  # 你的数据库用户名
        'PASSWORD': '',  # 你的数据库密码
        'HOST': '127.0.0.1',  # 你的数据库主机，留空默认为localhost
        'PORT': '3306',  # 你的数据库端口
    }


