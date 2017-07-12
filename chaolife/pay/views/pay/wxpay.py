import threading
import requests
import random
import hashlib
from urllib.parse import quote
import xml.etree.ElementTree as ET
from datetime import datetime
from datetime import timedelta
import time
from pay import config
from pay.config import WxPayConfig

class Singleton(object):
    _instance_look = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,"_instance"):
            with cls._instance_look:
                if not hasattr(cls,"_instance"):
                    impl = cls.configure() if hasattr(cls,"configure") else cls
                    instance = super(Singleton,cls).__new__(impl,*args,**kwargs)
                    if not isinstance(instance,cls):
                        instance.__init__(*args,**kwargs)
                    cls._instance = instance
                return cls._instance

class RequestsClient(object):
    xml_headers = {'Content-Type':'application/xml'}

    def get(self,url,second =30):
        from requests import request
        return requests.get(url,timeout=second)

    def postXml(self,xml,url,second=30):
        return self.postXmlSSL(xml,url,second=second,cert=False,post=True)

    def postXmlSSL(self,xml,url,second,cert,post):
        if cert:
            raise RuntimeError('未实现')
        if post:
            print('签名是{}'.format(xml))
            return requests.post(url=url,headers = self.xml_headers,data=xml.encode(encoding="utf-8"),timeout=second).content

class HttpClient(Singleton):
    @classmethod
    def configure(cls):
        return RequestsClient

class BaseApiClient(object):
    def trimString(self,value):
        if value is not None and len(value) == 0:
            value = None
        return value

    def createNoncestr(self,length =32):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0,len(chars))])
        return "".join(strs)

    def formatBizQueryParaMap(self,paraMap,urlencode):
        slist = sorted(paraMap)
        buff = []
        for k in slist:
            v = quote(paraMap[k]) if urlencode else paraMap[k]
            buff.append("{0}={1}".format(k,v))
        return "&".join(buff)

    def getSign(self,obj):
        # return 'E6CDC6187E19D945D43FC95AE8B47904'
        paramsStr = self.formatBizQueryParaMap(obj,False)
        paramsStr = "{0}&key={1}".format(paramsStr,WxPayConfig.KEY)
        print('待签名字符{}'.format(paramsStr))
        paramsStr = hashlib.md5(paramsStr.encode(encoding='utf-8')).hexdigest()
        result_ = paramsStr.upper()
        return result_

    def arrayToXml(self, arr):
        """array转xml"""
        xml = ["<xml>"]
        a = dict()

        for k, v in arr.items():
            xml.append("<{0}>{1}</{0}>".format(k, v))
            # if v.isdigit():
            #     xml.append("<{0}>{1}</{0}>".format(k, v))
            # else:
            #     xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    def xmlToArray(self, xml):
        """将xml转为array"""
        array_data = {}
        root = ET.fromstring(xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return array_data

    def postXmlCurl(self, xml, url, second=30):
        """以post方式提交xml到对应的接口url"""
        return RequestsClient().postXml(xml, url, second=second)

    def postXmlSSLCurl(self, xml, url, second=30):
        """使用证书，以post方式提交xml到对应的接口url"""
        return RequestsClient().postXmlSSL(xml, url, second=second)

class WxPayApiClient(BaseApiClient):
    """
    请求的接口基类
    """

    def __init__(self):
        self.url = None
        self.curl_timeout = 30
        self.parameters = {} # 请求参数，类型为关联数组
        self.result = {} #响应内容，类型为关联数组
        self.response = None

    def setParamter(self,paramter,paramterValue):
        self.parameters[self.trimString(paramter)] = self.trimString(str(paramterValue))

    def createXml(self):
        self.parameters["appid"] = WxPayConfig.APPID
        self.parameters["mch_id"] = WxPayConfig.MCHID
        self.parameters["nonce_str"] = self.createNoncestr()
        self.parameters = self.getSign(self.parameters) #生成签名
        return self.arrayToXml(self.parameters)

    def postXml(self):
        # check url is setting
        if self.url is None:
            raise KeyError('未设置WeiXin Pay url')
        xml = self.createXml()

        self.response = self.postXmlCurl(xml,self.url,self.curl_timeout)
        print('得到响应{}'.format(self.response))
        return self.response

    def postXmlSSL(self):
        xml = self.createXml()
        self.response = self.postXmlCurl(xml,self.url,self.curl_timeout)
        return self.response

    def getResult(self):
        self.postXml()
        self.result = self.xmlToArray(self.response)

        return self.result


class UnifiedOrderClient(WxPayApiClient):
    """

    """

    necessary_params = ("out_trade_no", "body", "total_fee", "notify_url", "trade_type")

    """统一支付接口类"""
    def __init__(self,timeout = WxPayConfig.CURL_TIMEOUT):
        super(UnifiedOrderClient,self).__init__()
        self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        self.curl_timeout = timeout
    def createXml(self):
        """生成接口参数xml"""
        # 检测必填参数
        print('调用createxml')
        for key in self.necessary_params:
            if self.parameters.get(key) is None:
                raise ValueError("mission paramter{}".format(key))
        if self.parameters["trade_type"] == "JSAPI" and self.parameters["openid"] is None:
            raise ValueError("JSAPI need openid parameters")

        self.parameters["appid"] = WxPayConfig.APPID  # 公众账号ID
        self.parameters["mch_id"] = WxPayConfig.MCHID  # 商户号
        self.parameters["nonce_str"] = self.createNoncestr(32)   # 随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  # 签名

        print(self.parameters)
        return self.arrayToXml(self.parameters)

    def getPrepayId(self):
        """获取prepay_id"""
        self.postXml()
        self.result = self.xmlToArray(self.response)
        print(self.result)
        prepay_id = self.result["prepay_id"]
        return prepay_id

    def getClientPayVertifi(self):
        #签名 appid nonceStr package partnerId prepayid timeStamp
        """
        再次签名，获得客户端所需要的 发起支付信息
        :return:
        """
        prepayid = self.getPrepayId()
        vertifyDict = {
            'appid':WxPayConfig.APPID,
            'noncestr':self.parameters.get('nonce_str'),
            'package':'Sign=WXPay',
            'partnerid':WxPayConfig.MCHID,
            'timestamp':int(datetime.now().timestamp()),
            'prepayid':prepayid,
        }
        sign = self.getSign(vertifyDict)
        vertifyDict['sign']=sign
        return vertifyDict


def test():
    print('测试一次')
    c = UnifiedOrderClient()
    c.setParamter("out_trade_no","123451")
    c.setParamter("body","Chao活-积分充值")
    c.setParamter("total_fee","100")
    c.setParamter("spbill_create_ip","14.23.150.211")
    c.setParamter("time_expire", "{:%Y%m%d%H%M%S}".format(datetime.now()+timedelta(minutes=WxPayConfig.ORDER_EXPIRE_TIME)))
    c.setParamter("trade_type","APP")
    c.setParamter("notify_url",WxPayConfig.NOTIFY_URL)
    c.getPrepayId()


if __name__ == '__main__':
    test()