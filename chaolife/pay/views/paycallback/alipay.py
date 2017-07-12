# -*- coding:utf-8 -*-
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from ...models import PointPay
from message.tasks import simple_notify_user
from account.models import BillHistory, User
from django.db import transaction
from django.core.mail import send_mail
import xml.etree.ElementTree as ET


def sendEmailToAdmin(request):
    send_mail('积分充值', str(request.body), 'chaomengshidai@agesd.com', ['nimdanoob@163.com'], )


def xmlToArray(xml):
    """将xml转为array"""
    array_data = {}
    root = ET.fromstring(xml)
    for child in root:
        value = child.text
        array_data[child.tag] = value
    return array_data


def parseAlipayCallback(request):
    pass


def parseZfbCallback(request):
    pass


@api_view(['POST', ])
def alipay_notify(request):
    sendEmailToAdmin(request)
    trade_status = request.POST.get('trade_status', None)
    if trade_status == 'TRADE_SUCCESS':
        trade_success = True
    else:
        trade_success = False
    out_trade_no = request.POST.get('out_trade_no', None)

    if trade_success:
        PointPay.handle_pay_succcess(out_trade_no=out_trade_no)
        # 是否是首冲用户
        return Response('success')
    else:
        return Response('失败')


@api_view(['POST','GET'],)
def wxpay_notify(request):
    print('哈哈支付')
    sendEmailToAdmin(request)
    callback_array = xmlToArray(request.body)
    print('解析是{}'.format(callback_array))
    if callback_array.get('return_code') == 'SUCCESS':
        trade_no = callback_array.get('out_trade_no')
        if trade_no:
            PointPay.handle_pay_succcess(out_trade_no=trade_no)
            response_xml = "<xml>\
                                <return_code><![CDATA[SUCCESS]]></return_code>\
                                <return_msg><![CDATA[OK]]></return_msg>\
                         </xml>"
            return Response(data=response_xml,content_type="application/xml")
    return Response('fail')


def getPayCompany(request):
    if request.POST.get('trade_status'):
        return PointPay.PAY_METHOD_ZFB
    elif request.POST.get('return_code'):
        return PointPay.PAY_METHOD_WX
