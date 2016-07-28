"""
Django settings for hotelBookingProject project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import django
import manage
import datetime
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
BASE_DIR = os.path.dirname(os.path.realpath(manage.__file__))
STATICFILES_DIRS = (
)
STATIC_URL = '/static/'
# 以下的配置是自己加的
# 当运行 python manage.py collectstatic 的时候
# STATIC_ROOT 文件夹 是用来将所有STATICFILES_DIRS中所有文件夹中的文件，以及各app中static中的文件都复制过来
# 把这些文件放到一起是为了用apache等部署的时候更方便
# 当调用collect staticfile时 放置的文件夹
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
print('static root is {}'.format(STATIC_ROOT))
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3p25-g&26g!kq%7bpqe1qxq^xa9hzgw)d)b_*7bf0iv8^kbiyt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# support celery
import djcelery
# BROKER_URL = 'redis://:Zhuo8995588@3e5069637587473d.redis.rds.aliyuncs.com:6379/DB0'
# todo 注意，我在 celery.py中覆盖了这些行为
BROKER_URL = 'django://'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler' # 定时任务
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'  #配置结果的存储
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = False # 不是用UTC
CELERY_TASK_RESULT_EXPIRES = 10 #任务结果的时效时间
CELERYD_LOG_FILE = BASE_DIR + "/logs/celery/celery.log" # log路径
CELERYBEAT_LOG_FILE = BASE_DIR + "/logs/celery/beat.log" # beat log路径

# Application definition

INSTALLED_APPS = [
    'redis_cache',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',#它将确保为你安装的应用中的每个Django模型创建3个默认的权限- add 、changed、delete
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'rest_framework',
    'dynamic_rest',
    'grappelli.dashboard',
    'grappelli',
    'rest_framework.authtoken',
    'debug_toolbar',
    'guardian',
    'hotelBooking',
    'djcelery',
    'kombu.transport.django',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',#它向每个接受到的HttpRequeset对象添加user属性，表示当前登入的用户
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'hotelBookingProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hotelBookingProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
from hotelBookingProject import dbconfig
DATABASES = dbconfig.get_config(testing=True).DATABASES

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
    'guardian.backends.ObjectPermissionBackend',
)


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
USE_TZ = False

USE_I18N = True

USE_L10N = True

INTERNAL_IPS = ('127.0.0.1',)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/



# 是否最后可以 不加 splash
APPEND_SLASH = True

AUTH_USER_MODEL = 'hotelBooking.User'

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
# session setting
SESSION_COOKIE_AGE = 365*24*60*60

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(STATIC_ROOT+'/logs/','all'+str(datetime.datetime.today().date())+'.log'), #或者直接写路径：'c:\logs\all.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(STATIC_ROOT+'/logs/','script.log'), #或者直接写路径：'filename':'c:\logs\request.log''
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'scprits_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(STATIC_ROOT+'/logs/','script.log'), #或者直接写路径：'filename':'c:\logs\script.log'
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default','console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'XieYin.app':{
            'handlers': ['default','console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'scripts': { # 脚本专用日志
            'handlers': ['scprits_handler'],
            'level': 'INFO',
            'propagate': False
        },
    }
}


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
          'rest_framework.authentication.BasicAuthentication',
          'rest_framework.authentication.TokenAuthentication',
    ),
   'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'hotelBooking.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 3,
    'EXCEPTION_HANDLER' : 'hotelBooking.utils.exceptionhandler.exception_handler',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION':'0.1'
}


DYNAMIC_REST = {
    # DEBUG: enable/disable internal debugging
    'DEBUG': True,

    # ENABLE_BROWSABLE_API: enable/disable the browsable API.
    # It can be useful to disable it in production.
    'ENABLE_BROWSABLE_API': True,

    # ENABLE_LINKS: enable/disable relationship links
    'ENABLE_LINKS': False,

    # ENABLE_SERIALIZER_CACHE: enable/disable caching of related serializers
    'ENABLE_SERIALIZER_CACHE': True,

    # ENABLE_SERIALIZER_OPTIMIZATIONS: enable/disable representation speedups
    'ENABLE_SERIALIZER_OPTIMIZATIONS': True,

    # DEFER_MANY_RELATIONS: automatically defer many-relations, unless
    # `deferred=False` is explicitly set on the field.
    'DEFER_MANY_RELATIONS': False,

    # MAX_PAGE_SIZE: global setting for max page size.
    # Can be overriden at the viewset level.
    'MAX_PAGE_SIZE': None,

    # PAGE_QUERY_PARAM: global setting for the pagination query parameter.
    # Can be overriden at the viewset level.
    'PAGE_QUERY_PARAM': 'page',

    # PAGE_SIZE: global setting for page size.
    # Can be overriden at the viewset level.
    'PAGE_SIZE': True,

    # PAGE_SIZE_QUERY_PARAM: global setting for the page size query parameter.
    # Can be overriden at the viewset level.
    'PAGE_SIZE_QUERY_PARAM': 'per_page',

    # ADDITIONAL_PRIMARY_RESOURCE_PREFIX: String to prefix additional
    # instances of the primary resource when sideloading.
    'ADDITIONAL_PRIMARY_RESOURCE_PREFIX': '+',

    # Enables host-relative links.  Only compatible with resources registered
    # through the dynamic router.  If a resource doesn't have a canonical
    # path registered, links will default back to being resource-relative urls
    'ENABLE_HOST_RELATIVE_LINKS': True,
    'DEFAULT_PAGINATION_CLASS': 'hotelBooking.pagination.StandardResultsSetPagination',
}

# 文件系统设置
QINIU_ACCESS_KEY = 'u-ryAwaQeBx9BS5t8OMSPs6P1Ewoqiu6-ZbbMNYm'
QINIU_SECRET_KEY = 'hVXFHO8GusQduMqLeYXZx_C5_c7D-VSwz6AKhjZJ'
QINIU_BUCKET_NAME = 'hotelbook'
QINIU_BUCKET_DOMAIN = 'qiniu.agesd.com'
QINIU_SECURE_URL = False
DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuStorage'


REDIS_TIMEOUT=7*24*60*60
CUBES_REDIS_TIMEOUT=60*60
NEVER_REDIS_TIMEOUT=365*24*60*60

