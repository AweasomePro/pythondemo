from django.conf.urls import patterns, url
from rest_framework import routers

from hotelBooking.views.product import housepackage
from hotelBooking.views.province import ProvinceViewSet
router = routers.SimpleRouter(trailing_slash=True,)
# city_router = routers.NestedSimpleRouter(nested_router,r'city',lookup='city')
# city_router.register(r'')
urlpatterns = [
    url(r'^order/hotel/$',housepackage.book_house_package),
]
urlpatterns += router.urls