from sms.client import SmsCodeChecker
from sms.models import SmsRecord
from common.exceptions import ConditionDenied,SmsCodeCheckFaield
class BaseLogicChecker(SmsCodeChecker):
    def __init__(self,request,business_type,*args,**kwargs):
        self.request = request
        self.need_business_type = business_type
        super(BaseLogicChecker,self).__init__(*args,**kwargs)
    def check(self):
        super(BaseLogicChecker,self).check()
        smsRecord = self.get_smsRecord()
        business_type = smsRecord.business_type
        print(business_type)
        print(self.need_business_type)
        if int(business_type) != self.need_business_type:
            raise SmsCodeCheckFaield()
        return True


class RegisterSmsChecker(BaseLogicChecker):
    need_business_type = SmsRecord.BUSINESS_TYPE_REGISTE
    def __init__(self,*args,**kwargs):
        super(RegisterSmsChecker,self).__init__(business_type=SmsRecord.BUSINESS_TYPE_REGISTE,*args,**kwargs)


class LoginSmsChecker(BaseLogicChecker):
    need_business_type = SmsRecord.BUSINESS_TYPE_LOGIN

class VertifySmsChecker(BaseLogicChecker):
    pass


def vertifySmsCode(request,business_type,):
    business_id = request.POST.get('business_id')
    sms_code = request.POST.get('smsCode', None)
    return VertifySmsChecker(request=request, business_type=business_type, business_id=business_id,
                      vertify_code=sms_code).check()
# def VertifySmsChecker(business_type):





