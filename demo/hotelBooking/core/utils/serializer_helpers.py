from rest_framework.utils.serializer_helpers import ReturnDict


class Custom_ReturnDict(ReturnDict):
    def __init__(self, *args, **kwargs):
        self.message = kwargs.pop('message')
        super(ReturnDict, self).__init__(*args, **kwargs)

def wrapper_response_dict(data=None, code=100, message='success'):
    if(data == None):
        return {'code':code,'message':message}
    else:
        return {'code': code,'message':message,'result':data}