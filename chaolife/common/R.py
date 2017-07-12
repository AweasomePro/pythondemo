class String(object):
    VERTIFY_SMS_SENT = "验证码已发送"
    PHONE_EXISTED = "手机号已存在"
    REGISTER_SUCCESS = "注册成功"
    SMS_SEND = "验证码发送成功"
    SMS_FAILED = "验证码发送失败"
    VERTIFY_FAILED = "验证失败"
    REGISTER_SMS_VERTIFY_FAILED = "注册失败，验证码验证失败"
    MODIFY_SUCCESS = "修改成功"
    MODIFY_PAY_PWD_SUCCESS = "支付密码修改成功"
    MODIFY_PAY_PWD_FAILED = "支付密码验证失败"

    UPLOAD_SUCCESS = "上传成功"

    PERMISSION_NO_POWER = "角色不被允许"


class METHOD(object):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
