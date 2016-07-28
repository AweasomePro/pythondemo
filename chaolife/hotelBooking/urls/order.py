from django.conf.urls import patterns, url

from hotelBooking.views.order.customerorder import (CustomerHotelBookOrderList,
                                                    )
from hotelBooking.views.order.partner import orderviews as partner_order_views
from hotelBooking.views.order.util import DeleteAllOrderView
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