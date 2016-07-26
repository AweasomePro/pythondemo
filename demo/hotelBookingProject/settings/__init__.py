from .dev import *
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

