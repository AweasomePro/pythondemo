from six import string_types

from hotelBooking.module import leancloud_client


def request_sms_code(phone_number, idd='+86', sms_type = 'sms',template = None,params = None):
    """
    请求发送手机验证码
    :param phone_number: 需要验证的手机号码
    :param idd: 号码的所在国家代码，默认是86
    :param sms_types: 验证码发送方式，＇voice＇为语音,'sms'为段兴
    :param template: 短信模板
    :param params:
    :return: None
    """
    if not isinstance(phone_number,string_types):
        raise TypeError('phone_number must be a string')

    data = {
        'mobilePhoneNumber':phone_number,
        'smsType': sms_type,
        'IDD':idd,
    }

    if template is not None:
        data['template'] = template

    if params is not None:
        data.update(params)

    return leancloud_client.post('/requestSmsCode',params=data)

def verify_sms_code(phone_number,code):
    """
    在获取到手机验证码后，验证验证码是否正确，如果验证失败，则
    :param phone_number: 需要验证的手机号码
    :param code: 接收到的验证
    :return: None
    """
    params = {
        'mobilePhoneNumber': phone_number,
    }
    response = leancloud_client.post('/verifySmsCode/{0}'.format(code), params=params)
    if response.status_code == 200:
        return True, "Success"
    elif response.json().get('default_code', 0) == 603:
        # Invalid SMS default_code
        print(response.json()['default_code'])
        return False, "Invalid SMS default_code"
    else:
        return False, "尚未处理的错误"