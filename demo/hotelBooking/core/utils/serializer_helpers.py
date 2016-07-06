from rest_framework.utils.serializer_helpers import ReturnDict


class Custom_ReturnDict(ReturnDict):
    def __init__(self, *args, **kwargs):
        self.message = kwargs.pop('message')
        super(ReturnDict, self).__init__(*args, **kwargs)

def wrapper_dict(data,code=100,message='success'):
    return {'code':code,'message':message,'result':data}