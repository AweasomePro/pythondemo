from django.conf.urls import patterns, url
from hotelBooking.views.product.housepackage import HousePackageBookAPIView, CustomerHotelBookOrderList
from rest_framework import routers

from hotelBooking.views.product import housepackage
from hotelBooking.views.province import ProvinceViewSet
router = routers.SimpleRouter(trailing_slash=True,)
# city_router = routers.NestedSimpleRouter(nested_router,r'city',lookup='city')
# city_router.register(r'')
router.register('^customer/orders',CustomerHotelBookOrderList)
urlpatterns = [
    url(r'^hotel/book$',HousePackageBookAPIView.as_view()),
]
urlpatterns += router.urls