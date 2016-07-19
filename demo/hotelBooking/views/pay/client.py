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


subject = '积分充值'
@transaction.atomic()
@authentication_classes([JSONWebTokenAuthentication,])
@is_authenticated()
@api_view(['GET',])
def point_pay(request):
    number = request.POST('number')
    pay = Pay.objects.create(
        user = request.user,
        number = 100,
        total_price = 100,
    )
    tn = __split_uuid(pay.id)
    print('uuid is {}'.format(tn))
    url = alipay.create_direct_pay_by_user(
        tn =tn,
        subject = '商品一号',
        body = '这是一件商品',
        total_fee = 1
    )
    return Response(wrapper_response_dict(data={'url':url}))
    # alipay.create_direct_pay_by_user_url(
    #     out_trade_no = pay.id,
    #     subject = subject,
    #     total_fee= number,
    #     notify_url='your_order_notify_url',
    #     goods_type ='0'
    # )



def __split_uuid(value):
    value = uuid.UUID(value.replace('-', ''))
    return value
class PointPayView(views.APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        """
        :param point 积分数量
        :return:
        """
        point_number = request.GET.get('point',100)
        # pay = Pay.objects.create(
        #     user=request.user,
        #     number=point_number,
        #     total_price=100,
        # )
        url = alipay.create_direct_pay_by_user(
            tn=12345,
            subject=subject,
            body='商品详情',
            total_fee=100
        )
        print('hahaha{}'.format(url))
        return Response(wrapper_response_dict(data={'url':url}))



@api_view(['POST',])
def alipay_notify(request):
    print(request.POST)
    return Response('success')

