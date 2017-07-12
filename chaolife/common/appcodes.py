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
CODE_NEGATIVE_100_APP_ERROR = 1
# 正常
CODE_100_OK = 100

# 100-150 用户相关
# 500以上其他旁支相关



# 通用的验证码验证失败
CODE_SMS_ERROR = 11

# 手机号已经存在 不能注册
CODE_PHONE_IS_EXIST = 101

# 用户验证失败
CODE_USER_AUTHENTICATE_FAIL = 102

# 不存在该账号
CODE_USER_NOT_EXIST = 103

# 获取头像上传token成功
CODE_OBTAIN_AVATAR_TOKEN_SUCCESS = 104

# 设备号上传成功
CODE_UPLOAD_INSTALLATION_SUCCESS = 105

# 设备号已经上传过了
CODE_UPLOAD_INSTALLATION_FAILED_IS_EXISTED = 106

# 设备绑定用户成功
CODE_INSTALLATION_BIND_SUCCESS = 107

#用户资料不完整
CODE_CUSTOMER_PROFILE_IMPERFECT = -108

# 积分不足
POINT_NOT_ENOUGH = 110
CODE_PAY_PWD_AUTHENTIC_ERROR = 111
CODE_EXISTE_UNHANDLE_REDEMPTIONS = 112


CODE_INSTALLATION_BIND_FAILED = -207

# 绑定用户时，设备号没有上传到服务端，先上传
CODE_INSTALLATION_BIND＿FAILED_NOT_UPLOADED = 208






# 订单类全部以2开头
ORDER_REQUIRED = 201 # 用户请求订单
ORDER_ACCEPTED = 202 # 商家接收订单
ORDER_CANCELD_BY_CUSTOMER = 203 #用户取消订单
ORDER_CANCELD_BY_SELLER = 204 #商家取消订单
ORDER_HOTEL_EXIST_SAME_DAY_BUSINESS = 210 # 存在同区间的订单，需要先取消

# 旁支
CODE_CREDIT_CARD_NOT_SUPPORT = 501 #信用卡暂不支持
CODE_CREDIT_CARD_AUTHENTIC_ERROR = 502 #信用卡验证失败
CODE_CREDIT_CARD_NOT_PROVIDE = 503 #没有提供信用卡

# 商品类
CODE_THE_PRODUCT_IS_OFFLINE = 301 # 这个商品已经下线
CODE_THE_PRICE_IS_TO_LOW = 302 # 商品价格过低
CODE_EXIST_SAME_PRODUCT = 303 # 存在同类型资源()
CODE_PRODUCT_IS_CHECKING = 303 # 存在同类型资源()


#验证码类


SMS_VERIFY_FAILED = -500
#短信发送失败
SMS_SEND_FAILED= -501
#短信发送过于频繁
SMS_SEND_TOO_SHORT = -502
#短信发送请求缺少必要参数
SMS_SEND_PARAMS_LACK = -503
#发送短信时阿里返回的错误
SMS_ALI_ERROR = -504

