# -*- coding:utf-8 -*-
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views.pay.paypoint import PointPayView
from .views import PointPayView,alipay_notify,InvoicesViewSets,invoices,wxpay_notify

pay_router = DefaultRouter()
pay_router.register(r'invoices',viewset=InvoicesViewSets,base_name='invoices')

#有前缀pay
urlpatterns = [
    url(r'^point/$', PointPayView.as_view()),
    url(r'^alipay/callback/$', alipay_notify),
    url(r'^wxpay/callback/$', wxpay_notify),
    url(r'^max_invoices/',invoices.max_value)
]
urlpatterns += pay_router.urls