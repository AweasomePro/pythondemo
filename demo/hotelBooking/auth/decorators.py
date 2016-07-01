from hotelBooking import User
from hotelBooking.utils.AppJsonResponse import JSONWrappedResponse


def is_authenticated():
    def decorator(func):
        def wrapper(request, *args, **kw):
            if(isinstance(request.user,AnonymousUser)):
                print('草 没有通过验证啊')
                return JSONWrappedResponse(status=-1, message='未通过token验证')
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
                return JSONWrappedResponse(status=-1, message='用户未登入')
            return func(request, *args, **kw)

        return wrapper
    return decorator