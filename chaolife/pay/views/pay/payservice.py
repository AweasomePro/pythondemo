from pay.config import ALLOW_PAY_TYPE
from pay.models import PointPay
from . import wxpay,alipay
from .wxpay import UnifiedOrderClient, WxPayConfig
from datetime import datetime
from datetime import timedelta
from pay.config import BASE_URL
import json
# 一个订单 包括 商品订单号 商品描述  商品详情 总金额，
# 微信 还需要 终端IP

#  微信客户端需要  签名sign  商户号partnerid  预支付交易会话ID prepayid
#
#
# 微信的返回内容类似
# {
#     'result_code': 'SUCCESS',
#     'sign': '04400A1385ECD8325A0568E5A3CE296C',
#     'return_msg': 'OK',
#     'nonce_str': 'XPdVmHEaW3Bn3Nhd',
#     'prepay_id': 'wx20160918180108c7fe0f48000202270789',
#     'trade_type': 'APP',
#     'mch_id': '1388334702',
#     'return_code': 'SUCCESS',
#     'appid': 'wxa6dddfe6123d6d56'
# }




class PointPayClient(object):
    PAY_ALLOW_PAY_TYPE = ALLOW_PAY_TYPE
    #支付有效期
    default_pay_validity_minute = 30


    def __init__(self,trade_no=None,subject='积分充值',body='积分充值',total_fee = 0,pay_method = PointPay.PAY_METHOD_ZFB ,*args,**kwargs):
        self._infor = {
            'trade_no':trade_no,
            'subject':subject,
            'body':body,
            'total_fee':total_fee,
            'pay_method':pay_method
        }

        print('self _infor is {}'.format(self._infor))
        print('paymethod is {}'.format(self._infor.get('pay_method')) )
        self._infor.update(kwargs)
        pass

    def get_client_pay_certificate(self):
        """
        获得客户端 需要发起支付的凭证
        对于 支付宝，返回的是url
        对于 微信 返回的是Json
        :return:
        """
        #warn 注意 这里的类型是 int
        if str(self._infor.get('pay_method')) == str(PointPay.PAY_METHOD_ZFB):
            return self._get_zfb_pay_certificate()
        else:
            return self._get_wx_pay_certificate()

    def _get_zfb_pay_certificate(self):
        infor = self._infor
        return alipay.create_direct_pay_url(
            tn = infor.get('trade_no'),
            subject = infor.get('subject'),
            body = infor.get('body'),
            total_fee = infor.get('total_fee'),
        )

    def _get_wx_pay_certificate(self):
        """
               sign 签名
               prepayid 预支付交易会话ID
               partnerid 商户号ID  (即MCHID)
               :return:
               """
        infor = self._infor
        unifiedOrderClient = UnifiedOrderClient()
        unifiedOrderClient.setParamter("out_trade_no", infor.get('trade_no'))
        unifiedOrderClient.setParamter("body", infor.get('body'))
        #warn 微信的支付单位是分
        unifiedOrderClient.setParamter("total_fee", int(infor.get('total_fee') * 100))
        unifiedOrderClient.setParamter("spbill_create_ip", infor.get('client_ip'))
        # unifiedOrderClient.setParamter("time_expire",
        #                                "{:%Y%m%d%H%M%S}".format(datetime.now() + timedelta(minutes=30)))
        # print('过期时间{}'.format("{:%Y%m%d%H%M%S}".format(datetime.now() + timedelta(minutes=30))))
        unifiedOrderClient.setParamter("trade_type", "APP")
        unifiedOrderClient.setParamter("notify_url", WxPayConfig.NOTIFY_URL)

        orderResult = unifiedOrderClient.getClientPayVertifi()

        return json.dumps(orderResult)

    def add_params(self,key,value):
        self._infor[key] = value

