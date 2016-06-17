"""
Decorators for views based on HTTP headers.
"""

from .AppJsonResponse import JSONWrappedResponse

import logging
logger = logging.getLogger('zxw.request')

def necessary(*necessary_key):
    def decorator(func):
        def wrapper(request,*args,**kw):
            print(*necessary_key)
            for i in necessary_key:
                if not request.POST.get(i):
                    return JSONWrappedResponse( status=-1, message="缺少必要的参数"+str(i))
            return func(request,*args,**kw)
        return wrapper
    return decorator
