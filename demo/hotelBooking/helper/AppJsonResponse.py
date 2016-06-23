import datetime
import time
from django.http import JsonResponse
from rest_framework import response
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import OrderedDict
import json
from django.utils import timezone

class JSONWrappedResponse(JsonResponse):
    """
    An  HttpResponse that renders its content into JSON.
    """

    def __init__(self, data=None, status=100, message="success", token=None,**kwargs):
        # data is a OrderedDict
        res = {"status": status, "message": message, "timeStamp": int(timezone.now().timestamp()),}
        if not data is None:
            print('data is not null')
            res['res'] = data
            print(res)



        super(JSONWrappedResponse, self).__init__(res, **kwargs)

    def addKey_value(self,key,value):
        json.loads(self.data)


class DefaultJsonResponse(Response):
    def __init__(self, data=None, status=100, message="成功",**kwargs):
        # data is a OrderedDict
        res = {"status": status, "message": message, "timeStamp": int(timezone.now().timestamp()),}

        if not data is None:
            res['res'] = data
            print(res)
        else:
            print('data is null')

        for key in kwargs:
            res[key] = kwargs[key]
        super(DefaultJsonResponse, self).__init__(res)