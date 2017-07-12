# -*- coding:utf-8 -*-
from chaolifeProject.settings import TEST

if TEST:
    BASE_URL = 'http://114.55.144.169/api/'
else:
    BASE_URL = 'http://114.55.67.147/api/'

# --  支付方式--
PAY_TYPE_ZFB = 'zhifubao'
PAY_TYPE_WX = 'weixin'
ALLOW_PAY_TYPE = (PAY_TYPE_ZFB,PAY_TYPE_WX)


class AliPayConfig:
    ALIPAY_NOTIFY_URL = BASE_URL + 'pay/alipay/callback/'
    # aliapy安全检验码，以数字和字母组成的32位字符
    ALIPAY_KEY = '200x3jvph6945seg5ylfg1xc4zhw32z1'

    ALIPAY_INPUT_CHARSET = 'utf-8'

    # 合作身份者ID，以2088开头的16位纯数字
    ALIPAY_PARTNER = '2088421443875084'

    # 签约支付宝账号或卖家支付宝帐户
    ALIPAY_SELLER_EMAIL = 'chaomengshidai@agesd.com'

    ALIPAY_SIGN_TYPE = 'RSA'

    # 付完款后跳转的页面（同步通知） 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    ALIPAY_RETURN_URL = ''

class WxPayConfig:
    APPID = "wxa6dddfe6123d6d56"
    # APPSECRET = "e5ff9db9ade7e8d695d048c85576cd47"
    MCHID = "1388334702"
    KEY = "e5ff9db9ade7e8d695d048c85576cd47"
    # APPSECRET = "e5ff9db9ade7e8d695d048c85576cd47"
    NOTIFY_URL = BASE_URL + 'pay/wxpay/callback/'
    CURL_TIMEOUT = 30
    ORDER_EXPIRE_TIME = 30