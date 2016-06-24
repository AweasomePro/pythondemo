"""
Descriptive HTTP status codes, for code readability.

See RFC 2616 - http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
And RFC 6585 - http://tools.ietf.org/html/rfc6585
"""
from __future__ import unicode_literals


def is_informational(code):
    return code >= 100 and code <= 199


def is_success(code):
    return code >= 200 and code <= 299


def is_redirect(code):
    return code >= 300 and code <= 399


def is_client_error(code):
    return code >= 400 and code <= 499


def is_server_error(code):
    return code >= 500 and code <= 599

# 程序应用错误
CODE_100_APP_ERROR = 1
# 正常
CODE_100_OK = 100

# 通用的验证码验证失败
CODE_SMS_ERROR = 101

# 登入成功
CODE_LOGIN_SUCCESS = 200

# 注册成功
CODE_REGISTER_SUCCESS = 201

# 手机号已经存在 不能注册
CODE_PHONE_IS_EXISTED = 202

# 用户验证失败
CODE_USER_AUTHENTICATE_FAIL = 203

# 获取头像上传token成功
CODE_OBTAIN_AVATAR_TOKEN_SUCCESS = 204

# 设备号上传成功
CODE_UPLOAD_INSTALLATION_SUCCESS = 205

# 设备号已经上传过了
CODE_UPLOAD_INSTALLATION_FAILED_IS_EXISTED = 206

# 设备绑定用户成功
CODE_INSTALLATION_BIND_SUCCESS = 207

# 绑定用户时，设备号没有上传到服务端，先上传
CODE_INSTALLATION_BIND＿FAILED_NOT_UPLOADED = 208

