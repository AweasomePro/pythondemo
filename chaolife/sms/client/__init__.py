import random

from sms import config
from top.api.base import RequestException
from top.api.rest import AlibabaAliqinFcSmsNumSendRequest
from . import exceptions
from .helper import SaveToDbMixin,SmsCodeChecker,send_notify_sms
from ._order_notify_helper import *

# 生成随机6位数字验证码
def generate_vertify_code():
    code_list = []
    for i in range(1, 7):
        code_list.append(str(random.randint(0, 9)))
    return ''.join(code_list)


class _VertifySmsReques(object):

    sms_free_sign_name = 'Chao活'

    def __init__(self,phone_number,):
        self._request_data_initialized = False
        self.aliSmsRequest = None
        self.request = AlibabaAliqinFcSmsNumSendRequest()
        self.sms_params = {}
        self.sms_template_code = None
        self.phone_number = phone_number
        self.code_generator = generate_vertify_code



    def _set_default_sms_params(self):
        self.sms_params['product'] = 'Chao活'
        self.sms_params['code'] = self.code_generator()

    def _set_default_request_info(self):
        self.request.sms_type = 'normal'
        self.request.extend = self.phone_number #回调的extend
        self.request.sms_free_sign_name = 'Chao活'
        self.request.rec_num = self.phone_number
        self.request.sms_template_code = self.sms_template_code
        self.request.sms_param = str(self.sms_params)


    def perform_request(self):
        self._set_default_sms_params()
        self._set_default_request_info()
        if self.request.sms_template_code == None:
            raise exceptions.SmsParmaslackException()
        try:
            print('准备发送请求')
            return self.request.getResponse()
        except RequestException:
            print('except 到 RequestException')
            raise exceptions.ConnectionAliSmsException

class VertifySmsRequest(SaveToDbMixin, _VertifySmsReques):
    def __init__(self,phone_number,template_code):
        super(VertifySmsRequest,self).__init__(phone_number)
        self.sms_template_code = template_code

class GetLoginSmsRequest(SaveToDbMixin, _VertifySmsReques):

    def __init__(self,phone_number):
        super(GetLoginSmsRequest,self).__init__(phone_number)
        self.sms_template_code = config.template_login_code

class RegisterSmsRequest(SaveToDbMixin, _VertifySmsReques):

    def __init__(self,phone_number):
        super(RegisterSmsRequest,self).__init__(phone_number=phone_number)
        self.sms_template_code = config.template_register_code


