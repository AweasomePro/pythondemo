#-*- coding: utf-8 -*-
from rest_framework.response import Response
from django.utils import timezone

class DefaultJsonResponse(Response):
    def __init__(self, data=None, code=100, message="成功", **kwargs):
        # data is a OrderedDict
        res = {
            "code": code,
            "message": message,
            "timeStamp": int(timezone.now().timestamp()),
            'result':data
        }
        super(DefaultJsonResponse, self).__init__(data=res,**kwargs)