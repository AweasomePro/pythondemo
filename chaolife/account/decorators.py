#-*- coding: utf-8 -*-
from common.utils.AppJsonResponse import DefaultJsonResponse


def only_customer(method):
    def wrapper(request,*args,**kwargs):
        if not (request.user and request.user.is_customer_member):
            return DefaultJsonResponse(message='必须是客户端用户才能访问该接口',data=-100)
        return method(request,*args,**kwargs)
    return wrapper


def only_hotel_partner(method):
    def wrapper(request,*args,**kwargs):
        if not (request.user and request.user.is_partner_member):
            return DefaultJsonResponse(message='必须是客户端用户才能访问该接口',data=-100)
        return method(request,*args,**kwargs)
    return wrapper