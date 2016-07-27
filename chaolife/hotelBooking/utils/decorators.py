"""
Decorators for views based on HTTP headers.
"""

from .AppJsonResponse import JSONWrappedResponse
from django.contrib.auth.models import AnonymousUser
import logging
logger = logging.getLogger('zxw.request')


def parameter_necessary(*necessary_key,optional=None):
    def decorator(func):
        def wrapper(request, *args, **kw):
            # todo 使用 set判断元素是否在其中，可以带来性能上的提升
            print(request.method)
            if request.method == 'POST':
                params = request.POST
                print(params)
            elif request.method == 'GET':
                params = request.GET
                print(params)
            else:
                # 如果 不是 'POST' 'GET',不做处理
                return func(request, *args, **kw)
            dict = {}
            for i in necessary_key:
                print('求{}'.format(i))
                if i in params:
                    dict[i]= request.POST.get(i) or request.GET.get(i)
                    print('从请求中得到{}'.format(dict[i]))
                else:
                    return JSONWrappedResponse(code=-1, message="缺少必要的参数" + str(i))
            kw.update(dict)
            opt_dict ={}
            if(optional is not None):
                for i in optional:
                    if i in params:
                        print('{0}在{1}中'.format(i, params))
                        opt_dict[i] = request.POST.get(i) or request.GET.get(i)
                    else:
                        print('{0}不在{1}中'.format(i, params))
                        opt_dict[i] = None
            kw.update(opt_dict)

            return func(request, *args, **kw)
        return wrapper
    return decorator


def method_route(methods=None, **kwargs):
    """
    Used to mark a method on a ViewSet that should be routed for list requests.
    """
    methods = ['get'] if (methods is None) else methods

    def decorator(func):
        func.bind_to_methods = methods
        func.detail = False
        func.kwargs = kwargs
        return func
    return decorator

def is_authenticated():
    def decorator(func):
        def wrapper(request, *args, **kw):
            if(isinstance(request.user,AnonymousUser)):
                print('草 没有通过验证啊')
                print(request.user)
                return JSONWrappedResponse(code=-1, message='未通过token验证')
            return func(request,*args,**kw)
        return wrapper
    return decorator

# _____________________________________________________order ___________________________________________________________