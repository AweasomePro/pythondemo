#-*- coding: utf-8 -*-
from django.contrib.auth.models import AnonymousUser
from chaolife.models import User
from chaolife.utils.AppJsonResponse import DefaultJsonResponse

def is_authenticated():
    def decorator(func):
        def wrapper(request, *args, **kw):
            if(isinstance(request.user,AnonymousUser)):
                print('草 没有通过验证啊')
                return DefaultJsonResponse(code=-1, message='未通过token验证')
            return func(request,*args,**kw)
        return wrapper
    return decorator
def login_required_and_is_member():
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    def decorator(func):
        def wrapper(request, *args, **kw):
            if (not isinstance(request.user, User)):
                print('草 没有通过验证啊')
                return DefaultJsonResponse(code=-1, message='用户未登入')
            return func(request, *args, **kw)

        return wrapper
    return decorator
def login_required_and_is_partner():
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    def decorator(func):
        def wrapper(request, *args, **kw):
            user = request.user
            if (not isinstance(user, User)):
                print('草 没有通过验证啊')
                return DefaultJsonResponse(code=-1, message='用户未登入')
            if user.partnermember is  None:
                return DefaultJsonResponse(code=-1, message='不是合作伙伴')
            print('permission ')
            return func(request, *args, **kw)
        return wrapper
    return decorator