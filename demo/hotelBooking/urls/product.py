from rest_framework_nested import routers
from django.conf.urls import patterns, url
from rest_framework.routers import SimpleRouter

from hotelBooking.views.hotel import HouseViewSet
from hotelBooking.views.product.housepackage import HousePackageView

house_simple_router = SimpleRouter(trailing_slash=False,)
house_simple_router.register('housepackage', HousePackageView)

urlpatterns = []
urlpatterns += house_simple_router.urls