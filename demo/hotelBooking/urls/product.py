from rest_framework_nested import routers
from django.conf.urls import patterns, url
from rest_framework.routers import SimpleRouter,DefaultRouter
from hotelBooking.views.hotel import RoomViewSet
from hotelBooking.views.product.roompackage import RoomPackageView,AddRoomPackageView, RoomPackageStateView
from hotelBooking.views.product import  roompackage as RoomPackageViews


house_simple_router = SimpleRouter(trailing_slash=False,)

house_simple_router.register('^roompackage', RoomPackageView)
house_simple_router.register('^roomstate', RoomPackageStateView)


urlpatterns = [
    url('^product/roompackage/add', RoomPackageViews.create_new_hotelpackage),

]
urlpatterns += house_simple_router.urls