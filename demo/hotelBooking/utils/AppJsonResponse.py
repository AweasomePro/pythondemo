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

    def __init__(self, data=None, code=100, message="success", token=None, **kwargs):
        # data is a OrderedDict
        res = {"code": code, "message": message, "timeStamp": int(timezone.now().timestamp()),}
        if not data is None:
            print('data is not null')
            res['result'] = data
            print(res)
        super(JSONWrappedResponse, self).__init__(res, **kwargs)

    def addKey_value(self,key,value):
        json.loads(self.data)


class DefaultJsonResponse(Response):
    def __init__(self, res_data=None, code=100, message="成功", **kwargs):
        # data is a OrderedDict
        res = {"code": code, "message": message, "timeStamp": int(timezone.now().timestamp()),}
        print('返回code 哦')
        if not res_data is None:
            res['result'] = res_data
        else:
            print('data is null')

        super(DefaultJsonResponse, self).__init__(data=res,**kwargs)