# -*- coding:utf-8 -*-
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views
order_router = DefaultRouter()
urlpatterns = [
    url(r'^refund/order_(?P<order>[0-9]+)', views.require_refund),
]
