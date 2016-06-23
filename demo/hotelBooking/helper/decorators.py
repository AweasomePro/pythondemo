"""
Decorators for views based on HTTP headers.
"""

from .AppJsonResponse import JSONWrappedResponse

import logging
logger = logging.getLogger('zxw.request')


def parameter_necessary(*necessary_key):
    def decorator(func):
        def wrapper(request,*args,**kw):
            print(*necessary_key)
            for i in necessary_key:
                if i in request.POST or i in request.GET:
                    pass
                else:
                    return JSONWrappedResponse(status=-1, message="缺少必要的参数" + str(i))
            return func(request,*args,**kw)
        return wrapper
    return decorator



