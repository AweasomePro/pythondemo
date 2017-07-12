#-*- coding: utf-8 -*-
from rest_framework_nested import routers
from chaolife.views import hotel
from rest_framework.routers import SimpleRouter, DefaultRouter

from chaolife.views.hotel import RoomTypesViewSet
from .city import nested_router as city_nested_router

nested_router = routers.NestedSimpleRouter(city_nested_router, r'city', lookup='city', trailing_slash=False)
nested_router.register(r'$hotels', hotel.HotelViewSet)

hotel_default_router = DefaultRouter()

hotel_default_router.register('hotels', hotel.HotelViewSet, base_name='hotels')
hotel_default_router.register('hotel', hotel.HotelDetialView, base_name='hotel')

hotel_types_router = routers.NestedSimpleRouter(hotel_default_router, r'hotel', lookup='hotel')
hotel_types_router.register(r'roomtypes', RoomTypesViewSet, base_name='roomtypes')


urlpatterns = []
urlpatterns += nested_router.urls
urlpatterns += hotel_default_router.urls
urlpatterns += hotel_types_router.urls