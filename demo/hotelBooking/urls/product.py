from rest_framework_nested import routers
from django.conf.urls import patterns, url
from rest_framework.routers import SimpleRouter,DefaultRouter
from hotelBooking.views.hotel import RoomViewSet
from hotelBooking.views.product.roompackage import HousePackageView,AddHousePackageView
from hotelBooking.views.product import  roompackage as RoomPackageViews


house_simple_router = SimpleRouter(trailing_slash=False,)

house_simple_router.register('^housepackage', HousePackageView)

urlpatterns = [
    url('^product/roompackage/add', RoomPackageViews.create_new_hotelpackage),
]
urlpatterns += house_simple_router.urls