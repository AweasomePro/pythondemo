from sms.client.exceptions import VertifySmsBaseException
from sms.models import SmsRecord
from . import exceptions
from top.api.rest import AlibabaAliqinFcSmsNumSendRequest

class SaveToDbMixin(object):
    # business_id = models.UUIDField(help_text='前端发送过来验证的唯一标识')
    # phone_number = models.CharField(max_length=20, help_text='发送的手机号')
    # user = models.ForeignKey(User, help_text='发送给的用户', null=True, on_delete=models.SET_NULL)
    # state = models.IntegerField(choices=SMS_STATE_CHOICES)
    # vertify_code = models.CharField(verbose_name='验证码')
    # ali_code = models.IntegerField(help_text='阿里返回的code')
    # ali_template_code = models.CharField(help_text='发送时的短信模板')
    # ali_sub_code = models.CharField(help_text='阿里返回的sub_code')
    # ali_sub_msg = models.CharField(help_text='阿里返回的sub_msg')

    def perform_request(self): # 使用注解的方式也可以哦
        response = super(SaveToDbMixin,self).perform_request()
        request = self.request
        smsRecord = SmsRecord()
        SmsRecord.phone_number = request.rec_num
        SmsRecord.ali_code = response
        response['smsRecord'] = self._parse_ali_response(response)
        self.response = response
        return response

    def get_smsRecord(self):
        return self.response['smsRecord']

    def get_smsRecord_data(self):
        from ..serializers import SmsRecordSerializer
        data = SmsRecordSerializer(self.get_smsRecord()).data
        return data
    def _parse_ali_response(self,response):

        if response.get('error_response'):
            self._catch_error_case(response)

        send_response = response.get('alibaba_aliqin_fc_sms_num_send_response')
        result = send_response.get('result')
        request_id = send_response.get('request_id')
        error_code = result.get('error_code',0)
        success = bool(result.get('success'))
        state = None
        if success:
            state = SmsRecord.SMS_SEND_SUCCESS
        else:
            state = SmsRecord.SMS_SEND_FAILED

        smsRecord = SmsRecord(
            ali_code=error_code,
            phone_number=self.request.rec_num,
            state=state,
            vertify_code=self.sms_params.get('code'),
            ali_template_code = self.request.sms_template_code,
        )

        phone_number = self.phone_number
        from account.models import User
        try :
            user = User.objects.get(phone_number = phone_number)
            smsRecord.user = user
        except User.DoesNotExist:
            pass
        smsRecord.save()
        return smsRecord


    def _catch_error_case(self,response):
        error_response = response.get('error_response')
        if error_response:
            print('发生了错误')
            sub_code = error_response.get('sub_code')
            raise VertifySmsBaseException(detail=error_response.get('sub_msg','未知错误'))


def vertify_smscode(business_id,vertify_code,):
    try:
        smsRecord = SmsRecord.objects.filter(business_id=business_id).get()
        if smsRecord.vertify_code == vertify_code:
            return True,smsRecord
        else:
            return False,smsRecord
    except SmsRecord.DoesNotExist:
        #warn 验证错误
        pass


class SmsCodeChecker(object):

    def __init__(self,business_id,vertify_code):
        self.business_id = business_id
        print('')
        self.vertify_code = vertify_code
        self.is_checked =  False
        self.smsRecord = None
    def check(self):
        self.is_checked=True
        try:
            smsRecord = SmsRecord.objects.filter(business_id=self.business_id).get()
            self.smsRecord = smsRecord
            if smsRecord.vertify_code != self.vertify_code :
                raise exceptions.VertifySmsNotMatchException()
            elif smsRecord.state!= SmsRecord.SMS_SEND_SUCCESS:
                #warn 状态错误
                raise exceptions.VertifySmsNotMatchException()
            smsRecord.state = SmsRecord.SMS_VERTIFY_SUCCESS
            smsRecord.save()
        except SmsRecord.DoesNotExist:
            raise exceptions.VertifySmsNotMatchException()

    def get_smsRecord(self):
        if self.is_checked == False:
            raise RuntimeError("when you want get smsRecord ,you must invoked check method ")
        return self.smsRecord

    def __bool__(self):
        raise RuntimeError('why you want to invoke bool method,do you wan to check the sms code can veritfy success, if yes,you should invoke check method')

def send_notify_sms(phoneNumber,sms_template_code,sms_param):
    req = AlibabaAliqinFcSmsNumSendRequest()

    req.sms_type = "normal"
    req.sms_free_sign_name = "Chao活"
    req.sms_param = sms_param
    req.rec_num = phoneNumber
    req.sms_template_code = sms_template_code
    try:
        print(req.sms_param)
        resp = req.getResponse()
        print(resp)
        return resp
    except Exception  as  e:
        print(e)