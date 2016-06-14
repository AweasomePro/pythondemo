"""
Decorators for views based on HTTP headers.
"""

from .AppJsonResponse import JSONWrappedResponse

import logging
logger = logging.getLogger('zxw.request')

def necessary(*necessary_key):
    def decorator(func):
        def wrapper(request,*args,**kw):
            if (request.method == 'POST'):
                print(*necessary_key)
                for i in necessary_key:
                    if not request.POST.get(i):
                        return JSONWrappedResponse( status=-1, message="缺少必要的参数"+str(i))
                return func(request,*args,**kw)
            else:
                return JSONWrappedResponse( status=-2, message="错误的请求方式")
        return wrapper
    return decorator
