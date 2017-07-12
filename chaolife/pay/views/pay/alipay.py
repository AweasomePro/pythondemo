# -*- coding:utf-8 -*-
from urllib.parse import quote
from django.utils.encoding import smart_str
from .hashcompact import md5_constructor as md5
from pay.config import AliPayConfig
from collections import OrderedDict
#  字符串编码处理

# 网关地址
_GATEWAY =  'https://openapi.alipay.com/gateway.do?'

def gneranteUnsignedUrl(params):
    """
    字典拼接成 url
    :param params:
    :return:
    """
    ks = params.keys()
    prestr = ''
    for k in ks:
        v = params[k]
        k = smart_str(k, AliPayConfig.ALIPAY_INPUT_CHARSET)
        if k not in ('sign','sign_type') and v !='':
            params[k] = smart_str(v, AliPayConfig.ALIPAY_INPUT_CHARSET)
            prestr += '{}=\"{}\"&'.format(k,params[k])
    return prestr


def sign_pay_url(prestr, key, sign_type ='MD5'):
    """
    签名
    :param prestr: 未签字符串
    :param key:  秘钥
    :param sign_type: 签名类型
    :return:
    """
    if sign_type == 'MD5':
        return md5( (prestr + key).encode('utf-8')).hexdigest()
    elif sign_type == 'RSA':
        from chaolife.utils import cryptoutils
        # todo 注意  RSA不需要检验码，
        # 去掉最后一个 &
        return smart_str(quote(cryptoutils.sign_pkcs8(prestr[:-1]), safe=''))
    return ''


# 即时到账交易接口
def create_direct_pay_url(tn, subject, body, total_fee):
    params = OrderedDict()

    # 获取配置文件
    params['partner'] = AliPayConfig.ALIPAY_PARTNER
    params['seller_id'] = AliPayConfig.ALIPAY_PARTNER

    params['out_trade_no'] = tn  # 请与贵网站订单系统中的唯一订单号匹配
    params['subject'] = subject  # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['body'] = body  # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里，不可以为空
    params['total_fee'] = total_fee  # 订单总金额，显示在支付宝收银台里的“应付总额”里，精确到小数点后两位

    params['notify_url'] = AliPayConfig.ALIPAY_NOTIFY_URL
    # 从订单数据中动态获取到的必填参数
    params['service'] = 'mobile.securitypay.pay'
    params['payment_type'] = '1'  # 商品购买，只能选这个
    params['_input_charset'] = AliPayConfig.ALIPAY_INPUT_CHARSET
    params['it_b_pay'] = '30m'
    params['return_url'] = 'm.alipay.com'
    # 签名
    prestr = gneranteUnsignedUrl(params)
    #拼接
    sign = 'sign=\"{}\"&'.format(sign_pay_url(prestr, AliPayConfig.ALIPAY_KEY, AliPayConfig.ALIPAY_SIGN_TYPE))
    sign_type = 'sign_type=\"RSA\"'
    prestr = prestr+sign+sign_type
    return prestr

