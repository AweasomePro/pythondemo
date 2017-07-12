from .common import *
if os.name == 'nt': # 本机是window 系统
    from .prod import *
    TEST = True
    DEBUG = True
else:
    if os.environ.get('django_debug',None)  == 'True':
        print('测试')
        from .dev import *
        TEST = True
        DEBUG = True
    else:
        from .prod import *
        TEST = False
        DEBUG = False
