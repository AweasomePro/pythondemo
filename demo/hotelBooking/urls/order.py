from django.conf.urls import patterns, url

from hotelBooking.views.order.customerorder import (CustomerOrderActionAPIView, CustomerHotelBookOrderList,
                                                    RoomPackageBookAPIView)
from hotelBooking.views.order.util import DeleteAllOrderView
from rest_framework import routers


router = routers.SimpleRouter(trailing_slash=True,)
# city_router = routers.NestedSimpleRouter(nested_router,r'city',lookup='city')
# city_router.register(r'')
router.register('^customer/orders',CustomerHotelBookOrderList)

urlpatterns = [
    url(r'^hotel/book$', RoomPackageBookAPIView.as_view()),
    url(r'order/customer',CustomerOrderActionAPIView.as_view()),
    url(r'deleteorder',DeleteAllOrderView.as_view())
]
urlpatterns += router.urls