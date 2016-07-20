import uuid

from django.contrib.auth.decorators import login_required
from django.db import transaction
from hotelBooking.models.pay import Pay
from hotelBooking.utils.decorators import is_authenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import views
from rest_framework import viewsets,permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from . import alipay
from hotelBooking.views import wrapper_response_dict
from hotelBooking.models.order_utils import get_next_pay_order_number


subject = '积分充值'


class PointPayView(views.APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    @transaction.atomic()
    def get(self,request):
        """
        :param point 积分数量
        :return:
        """
        point_number = request.GET.get('point',100)
        trade_no = get_next_pay_order_number(request)
        print('trade_no 是{}'.format(trade_no))
        pay = Pay.objects.create(
            trade_no =trade_no,
            user=request.user,
            number=point_number,
            total_price=100,
        )
        url = alipay.create_direct_pay_by_user(
            tn=pay.trade_no,
            subject=subject,
            body='商品详情',
            total_fee=point_number
        )
        return Response(wrapper_response_dict(data={'url':url}))


def split_uuid(value):
    value = uuid.UUID(value.replace('-', ''))
    return value


@api_view(['POST',])
def alipay_notify(request):
    print(request.POST)
    return Response('success')

