# -*- coding:utf-8 -*-
from django.http import Http404
from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.decorators import detail_route,api_view
from common.viewsets import CustomDynamicModelViewSet
from .serializers import RefundOrderSerializer
from .models import OrderRefund
from chaolife.models.orders import Order,HotelPackageOrder
from rest_framework.response import Response
from common.exceptions import ResourceNotExist
class RefundOrderViewSets(CustomDynamicModelViewSet):
    serializer_class = RefundOrderSerializer
    queryset = OrderRefund.objects.all()


    @detail_route(methods=['GET',],url_path='require-refund')
    def require_refund(self,request,):
        return Response('测试中')
        pass



@api_view(('GET',),)
def require_refund(request,order,*args,**kwargs):
    try:
        order = Order.objects.get_subclass(number=order)
    except Order.DoesNotExist:
        raise ResourceNotExist
    if isinstance(order,HotelPackageOrder):
        print('yes is hotelPackage')
    return Response('测试中')
