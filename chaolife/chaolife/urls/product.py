#-*- coding: utf-8 -*-
from rest_framework_nested import routers
from rest_framework.routers import SimpleRouter,DefaultRouter
from chaolife.views.product.roompackage import RoomPackageView, RoomPackageStateView
from chaolife.views.product import PartnerRoomPackageView


house_simple_router = SimpleRouter(trailing_slash=True,)

house_simple_router.register('^partner/roompackage', PartnerRoomPackageView,base_name='partner_roompackage')
house_simple_router.register('^roompackage', RoomPackageView)
house_simple_router.register('^roomstate', RoomPackageStateView)


urlpatterns = [
    # url('^product/roompackage/add', RoomPackageViews.create_new_hotelpackage),
]
urlpatterns += house_simple_router.urls