import datetime
import time
from django.http import JsonResponse
from rest_framework import response
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import OrderedDict
from django.utils import timezone

class JSONWrappedResponse(JsonResponse):
    """
    An  HttpResponse that renders its content into JSON.
    """

    def __init__(self, data=None, status=1, message="success", **kwargs):
        # data is a OrderedDict
        res = {"status": status, "message": message, "timeStamp": timezone.now(),}
        if not data is None:
            print('data is not null')
            res['Res'] = data
            print(res)
        else:
            print('data is null')
        super(JSONWrappedResponse, self).__init__(res, **kwargs)
