from .common import *

DEBUG = True
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

# redis 缓存配置
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '3e5069637587473d.redis.rds.aliyuncs.com:6379',
        'PASSWORD':'Zhuo8995588',
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        },
    },
}
