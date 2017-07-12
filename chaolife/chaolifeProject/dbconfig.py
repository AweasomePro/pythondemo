# -*- coding:utf-8 -*-
#本地配置参数
class Test():
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
#服务器配置参数
class Production():
    # warning 生产环境数据库
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


def get_config(testing = True):
    if testing:
        return Test()
    else:
        return Production()
