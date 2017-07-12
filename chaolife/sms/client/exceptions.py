from common.exceptions import ConditionDenied
from common import appcodes
exception_code_map = {
    'isv.OUT_OF_SERVICE':'业务停机',
    'isv.MOBILE_NUMBER_ILLEGAL':'手机号码格式错误',
    'isv.MOBILE_COUNT_OVER_LIMIT':'手机号码数量超过限制',
    'isv.BUSINESS_LIMIT_CONTROL':'触发业务流控限制',
    'isv.AMOUNT_NOT_ENOUGH':'余额不足',
}




class VertifySmsBaseException(ConditionDenied):
    def __init__(self, detail=None, code = appcodes.SMS_ALI_ERROR,*args, **kwargs):
        if detail is None:
            self.detail = '未知短信错误'
        else:
            self.detail = detail
        super(VertifySmsBaseException,self).__init__(detail=self.detail,code = code,*args,**kwargs)


class SmsParmaslackException(VertifySmsBaseException):
    def __init__(self):
        super(SmsParmaslackException,self).__init__(detail='请求短信接口缺少参数',code=appcodes.SMS_SEND_PARAMS_LACK)

class ConnectionAliSmsException(VertifySmsBaseException):
    # ali的 错误，可能是限流之类的，有时间需要做细分
    def __init__(self):
        super(ConnectionAliSmsException,self).__init__(detail='发送过于频繁',code=appcodes.SMS_SEND_TOO_SHORT)


class VertifySmsNotMatchException(VertifySmsBaseException):
    def __init__(self):
        super(VertifySmsNotMatchException,self).__init__(detail='短信验证失败',code=appcodes.SMS_VERIFY_FAILED)