# -*- coding:utf-8 -*-
from ..serializers import InvoiceSerializer
from chaolife.permissions.rolepermissions import CustomerPermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from authtoken.authentication import TokenAuthentication
from rest_framework.decorators import detail_route, api_view,authentication_classes,permission_classes,list_route
from common.utils.AppJsonResponse import DefaultJsonResponse
from ..models import Invoice
from django.db import transaction
from common.viewsets import CustomDynamicModelViewSet
from common import exceptions
from common.exceptions import ConditionDenied
from common.decorators import parameter_necessary
@authentication_classes([TokenAuthentication])
@permission_classes([CustomerPermission])
@api_view(('GET',))
def max_value(request,):
    return DefaultJsonResponse(data={'max_value':request.user.customermember.max_invoices_value})

class InvoicesViewSets(CustomDynamicModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (CustomerPermission,)
    authentication_classes = (TokenAuthentication,)

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            data = request.data.copy()
            data['state'] =Invoice.STATE_REQUIRE
            #warn 是否存在异步导致的数据不同步问题
            data['user'] = request.user
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return DefaultJsonResponse(data= serializer.data,)

    @list_route(methods=['GET',],url_path = 'latest')
    def get_latest_invoice(self,request,*args,**kwargs):
        invoices = self.get_queryset().first()
        if invoices is not None:
            data = self.serializer_class(invoices).data
            return DefaultJsonResponse(data={'invoice':data})
        else:
            return DefaultJsonResponse(data=None,message='无历史提交信息')


    @detail_route(methods=['GET',],url_path = 'received')
    def read_invoice(self,request,*args,**kwargs):
        invoice = self.get_object()
        if invoice.state in (Invoice.STATE_SENDING,Invoice.STATE_REJECT):
            invoice.viewed = True
            invoice.save()
            data = self.serializer_class(invoice).data
            return DefaultJsonResponse(data={'invoice':data})
        else:
            raise exceptions.ConditionDenied(detail='错误的操作')

    @detail_route(methods=['POST'],url_path ='modify')
    def modify_email_or_content(self,request,pk,*args,**kwargs):
        invoice  = self.get_object()
        if invoice.state != Invoice.STATE_REQUIRE:
            raise ConditionDenied(detail='当前状态无法修改，详情咨询后台')
        email = request.data.get('email')
        title = request.data.get('title')
        type = request.data.get('type')
        if email:
            invoice.email = email
        if title:
            invoice.title = title
        if type:
            invoice.type = type
        invoice.save()
        return DefaultJsonResponse(message='成功', data={'invoice':InvoiceSerializer(invoice).data})



    def _support_modify_data(self,data):
        allow_data = {}
        title = data.get('title')
        email = data.get('email')
        if title:
            allow_data.pop('title',title)
        if email:
            allow_data.pop('email',email)
        return allow_data

    def get_queryset(self):
        return self.queryset.prefetch_related('user').filter(user=self.request.user)





