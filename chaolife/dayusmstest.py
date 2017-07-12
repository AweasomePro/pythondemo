import random

import top.api


req = top.api.AlibabaAliqinFcSmsNumSendRequest()


def generate_vertify_code():
    code_list = []
    for i in range(1,7):
        code_list.append( str(random.randint(0, 9)))
    return ''.join(code_list)

sms_param = {'code':generate_vertify_code(),'product':'潮生活'}
# sms_param = "{\"code\":\"1234\",\"product\":\"潮生活\"}"

# print(generate_vertify_code())
# print(type(generate_vertify_code()))
req.extend = "wocaonima"
req.sms_type = "normal"
req.sms_free_sign_name = "Chao生活"
req.sms_param = str(sms_param)
req.rec_num = "15726814574"
req.sms_template_code = "SMS_13390159"
resp = req.getResponse()

print(resp)
