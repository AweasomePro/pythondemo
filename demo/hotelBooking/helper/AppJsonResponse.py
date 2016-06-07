import datetime
import time
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import OrderedDict


class JSONWrappedResponse(JsonResponse):
    """
    An  HttpResponse that renders its content into JSON.
    """
    def __init__(self, data=None, status=1, message="success", **kwargs):
        # data is a OrderedDict
        res = {"status": status, "message": message, "responseTime":  time.mktime(datetime.datetime.now().timetuple()),}
        if not data is None:
            res.pop("res",data)

        super(JSONWrappedResponse, self).__init__(res,**kwargs)