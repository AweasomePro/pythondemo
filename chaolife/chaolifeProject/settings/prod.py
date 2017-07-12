DEBUG = False
# BROKER_URL = 'redis://Zhuo8995588@3e5069637587473d.redis.rds.aliyuncs.com:6379/0'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chaolife_prod',  # 你的数据库名称
        'USER': 'zhuoxiuwu',  # 你的数据库用户名
        'PASSWORD': 'Zhuo8995588',  # 你的数据库密码
        'HOST': 'rm-bp13c9g5jzm1vpg51o.mysql.rds.aliyuncs.com',  # 你的数据库主机，留空默认为localhost
        'PORT': '3306',  # 你的数据库端口
    }
}

# redis 缓存配置
# CACHES = {
#     'default':{
#         'BACKEND': 'redis_cache.RedisCache',
#         'LOCATION': 'redis-test.t0.daoapp.io:61107',
#     }
# }