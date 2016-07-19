from base64 import urlsafe_b64encode
from urllib.parse import urlencode

import types
from .hashcompact import md5_constructor as md5
from .config import settings

#  字符串编码处理

def smart_str(s,encodeing = 'utf-8',string_only = False,errors = 'strict'):
    return s
    # if string_only and isinstance(s,(types.NoneType,int)):
    #     return s

# 网关地址
_GATEWAY =  'https://openapi.alipay.com/gateway.do?'

def params_filter(params):
    ks = params.keys()
    ks = sorted(ks)
    newparams = {}
    prestr = ''
    for k in ks:
        v = params[k]
        k = smart_str(k,settings.ALIPAY_INPUT_CHARSET)
        if k not in ('sign','sign_type') and v !='':
            newparams[k] = smart_str(v,settings.ALIPAY_INPUT_CHARSET)
            prestr += '%s=%s&'.format(k,newparams[k])
    prestr = prestr[:-1]
    return newparams,prestr

def build_mysign(prestr,key,sign_type = 'MD5'):
    if sign_type == 'MD5':
        return md5( (prestr + key).encode('utf-8')).hexdigest()
    elif sign_type == 'RSA':
        from hotelBooking.utils import cryptoutils
        from urllib import parse
        return urlsafe_b64encode(cryptoutils.sign((prestr + key).encode('utf-8')))

    return ''


# 即时到账交易接口
def create_direct_pay_by_user(tn, subject, body, total_fee):
    params = {}
    params['service'] = 'mobile.securitypay.pay'
    params['payment_type'] = '1'  # 商品购买，只能选这个

    # 获取配置文件
    params['partner'] = settings.ALIPAY_PARTNER
    params['seller_id'] = settings.ALIPAY_SELLER_EMAIL
    # params['seller_email'] = settings.ALIPAY_SELLER_EMAIL
    params['return_url'] = settings.ALIPAY_RETURN_URL
    params['notify_url'] = settings.ALIPAY_NOTIFY_URL
    params['_input_charset'] = settings.ALIPAY_INPUT_CHARSET

    # 从订单数据中动态获取到的必填参数
    params['out_trade_no'] = tn  # 请与贵网站订单系统中的唯一订单号匹配
    params['subject'] = subject  # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['body'] = body  # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里，不可以为空
    params['total_fee'] = total_fee  # 订单总金额，显示在支付宝收银台里的“应付总额”里，精确到小数点后两位

    # # 扩展功能参数——网银提前
    # if bank == 'alipay' or bank == '':
    #     params['paymethod'] = 'directPay'  # 支付方式，四个值可选：bankPay(网银); cartoon(卡通); directPay(余额); CASH(网点支付)
    #     params['defaultbank'] = ''  # 支付宝支付，这个为空
    # else:
    #     params['paymethod'] = 'bankPay'  # 默认支付方式，四个值可选：bankPay(网银); cartoon(卡通); directPay(余额); CASH(网点支付)
    #     params['defaultbank'] = bank  # 默认网银代号，代号列表见http://club.alipay.com/read.php?tid=8681379

    params, prestr = params_filter(params)

    params['sign'] = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)
    params['sign_type'] = settings.ALIPAY_SIGN_TYPE

    return _GATEWAY + urlencode(params)