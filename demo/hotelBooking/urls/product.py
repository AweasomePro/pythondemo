from rest_framework_nested import routers
from django.conf.urls import patterns, url
from rest_framework.routers import SimpleRouter
from hotelBooking.views.hotel import HouseViewSet
from hotelBooking.views.product.housepackage import HousePackageView,AddHousePackageView
from hotelBooking.views.product import  housepackage as HousePackageViews


house_simple_router = SimpleRouter(trailing_slash=False,)

house_simple_router.register('housepackage', HousePackageView)

urlpatterns = [
    url('^product/housepackage/add',HousePackageViews.create_new_hotelpackage),
]
urlpatterns += house_simple_router.urls