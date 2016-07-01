from rest_framework_nested import routers
from django.conf.urls import patterns, url
from hotelBooking.views import hotel
from rest_framework.routers import SimpleRouter
from .city import nested_router as city_nested_router

nested_router = routers.NestedSimpleRouter(city_nested_router, r'city', lookup='city', trailing_slash=False)
nested_router.register(r'hotel', hotel.HotelViewSet)
hotel_simple_router = SimpleRouter()
hotel_simple_router.register('hotel', hotel.HotelViewSet)
urlpatterns = []
urlpatterns += nested_router.urls
urlpatterns += hotel_simple_router.urls