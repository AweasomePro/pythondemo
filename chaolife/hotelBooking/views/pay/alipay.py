# -*- coding:utf-8 -*-
from base64 import urlsafe_b64encode
from urllib.parse import urlencode,quote
from django.utils.encoding import smart_str
import types
from .hashcompact import md5_constructor as md5
from .config import settings
from collections import OrderedDict
#  字符串编码处理



# 网关地址
_GATEWAY =  'https://openapi.alipay.com/gateway.do?'

def params_filter(params):
    ks = params.keys()
    prestr = ''
    for k in ks:
        v = params[k]
        k = smart_str(k,settings.ALIPAY_INPUT_CHARSET)
        if k not in ('sign','sign_type') and v !='':
            params[k] = smart_str(v,settings.ALIPAY_INPUT_CHARSET)
            prestr += '{}=\"{}\"&'.format(k,params[k])
    return prestr

def build_mysign(prestr,key,sign_type = 'MD5'):
    # 去掉最后一个 &

    if sign_type == 'MD5':
        return md5( (prestr + key).encode('utf-8')).hexdigest()
    elif sign_type == 'RSA':
        from hotelBooking.utils import cryptoutils
        # todo 注意  RSA不需要检验码，
        print('需要做的解码是')
        print(prestr[:-1])
        return smart_str(quote(cryptoutils.sign((prestr[:-1]).encode('utf-8')),safe=''))
    return ''


# 即时到账交易接口
def create_direct_pay_by_user(tn, subject, body, total_fee):
    params = OrderedDict()

    # 获取配置文件
    params['partner'] = settings.ALIPAY_PARTNER
    params['seller_id'] = settings.ALIPAY_SELLER_EMAIL
    # params['out_trade_no'] = 123  # 请与贵网站订单系统中的唯一订单号匹配
    # params['subject'] = '商品详情'  # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    # params['body'] = '积分充值'  # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里，不可以为空
    # params['total_fee'] = '0.01'  # 订单总金额，显示在支付宝收银台里的“应付总额”里，精确到小数点后两位

    params['out_trade_no'] = tn  # 请与贵网站订单系统中的唯一订单号匹配
    params['subject'] = subject  # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['body'] = body  # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里，不可以为空
    params['total_fee'] = total_fee  # 订单总金额，显示在支付宝收银台里的“应付总额”里，精确到小数点后两位

    params['notify_url'] = settings.ALIPAY_NOTIFY_URL
    # 从订单数据中动态获取到的必填参数
    params['service'] = 'mobile.securitypay.pay'
    params['payment_type'] = '1'  # 商品购买，只能选这个
    params['_input_charset'] = settings.ALIPAY_INPUT_CHARSET
    params['it_b_pay'] = '30m'
    params['return_url'] = 'm.alipay.com'

    prestr = params_filter(params)

    sign = 'sign=\"{}\"&'.format(build_mysign(prestr,settings.ALIPAY_KEY,settings.ALIPAY_SIGN_TYPE))
    sign_type = 'sign_type=\"RSA\"'
    prestr = prestr+sign+sign_type
    return prestr

def getOrderInfo(subject,body,price):
    # orderInfo =
    pass