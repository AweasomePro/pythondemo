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
            print(request.method)
            print(request.POST)
            if request.method == 'POST':
                params = request.POST
            elif request.method == 'PUT':
                params = request.data
            else:
                # 如果 不是 'POST' 'GET',不做处理
                return func(request, *args, **kw)
            dict = {}
            for i in necessary_key:
                if i in params:
                    dict[i]= request.POST.get(i) or request.GET.get(i)
                    pass
                else:
                    return JSONWrappedResponse(status=-1, message="缺少必要的参数" + str(i))
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
                return JSONWrappedResponse(status=-1, message='未通过token验证')
            return func(request,*args,**kw)
        return wrapper
    return decorator

# _____________________________________________________order ___________________________________________________________