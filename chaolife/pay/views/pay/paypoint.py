# -*- coding:utf-8 -*-

import uuid
from django.db import transaction

from chaolife.models import HotelOrderNumberGenerator
from pay.models import PointPay
from authtoken.authentication import TokenAuthentication
from rest_framework import views
from rest_framework import permissions
from common.decorators import DefaultJsonResponse
from chaolife import app_settings
from common.utils import channelutil
from .payservice import PointPayClient
subject = '积分充值'


#/pay/point/
class PointPayView(views.APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic()
    def get(self,request):
        """
        :param point 积分数量
        :return:
        """
        # warn point 改成price
        money_number = int(request.GET.get('point',100))
        trade_no = HotelOrderNumberGenerator.get_next_pay_order()

        pay = PointPay.objects.create(
            trade_no =trade_no,
            user=request.user,
            number=money_number * app_settings.point_price, #为了测试，暂时全是100,注意是 int 类型，0.01 数据库会存成0
            total_price=money_number * 1,
            pay_method = self.pay_method
        )

        if app_settings.TEST: #测试服修改订单总价
            pay.total_price = 0.01
        # 生成支付客户端所需要的支付凭证
        client_ip = channelutil.get_client_ip(self.request)
        if client_ip == None:
            #warn 可能是测试账号
            client_ip = '10.91.229.211'
        payClient = PointPayClient(
            trade_no=pay.trade_no,
            subject='积分充值',
            body='积分充值',
            total_fee=pay.total_price,
            pay_method=self.pay_method)

        payClient.add_params('client_ip',client_ip)

        if request.version == '0.1':
            res_prefix='url'
        else:
            res_prefix = 'certifi'
        return DefaultJsonResponse(data={res_prefix:payClient.get_client_pay_certificate()})


    @property
    def pay_method(self):
        return self.request.GET.get('pay_method', PointPay.PAY_METHOD_ZFB)



def split_uuid(value):
    value = uuid.UUID(value.replace('-', ''))
    return value




