#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from chaolife.views.order.customerorder import (CustomerHotelBookOrderList,
                                                )
from chaolife.views.order.partner import orderviews as partner_order_views
from chaolife.views.order.util import DeleteAllOrderView
from rest_framework import routers


router = routers.SimpleRouter(trailing_slash=True,)
# city_router = routers.NestedSimpleRouter(nested_router,r'city',lookup='city')
# city_router.register(r'')
router.register('^customer/orders',CustomerHotelBookOrderList)
router.register('^partner/orders', partner_order_views.PartnerHotelOrderViewSet)
urlpatterns = [
    url(r'deleteorder',DeleteAllOrderView.as_view())
]
urlpatterns += router.urls