from rest_framework_nested import routers
from django.conf.urls import patterns, url
from hotelBooking.views import hotel
from rest_framework.routers import SimpleRouter, DefaultRouter

# from hotelBooking.views.hotel import RoomTypeViewSet
from .city import nested_router as city_nested_router

nested_router = routers.NestedSimpleRouter(city_nested_router, r'city', lookup='city', trailing_slash=False)
nested_router.register(r'$hotel', hotel.HotelViewSet)

# hotel_types_router = routers.NestedSimpleRouter(nested_router,r'hotel',lookup='hotel')
# hotel_types_router.register(r'types',RoomTypeViewSet,base_name='roomtypes')

hotel_default_router = DefaultRouter()
hotel_default_router.register('hotel', hotel.HotelViewSet, base_name='hotels')

hotel_types_router = routers.NestedSimpleRouter(hotel_default_router, r'hotel', lookup='hotel')
# hotel_types_router.register(r'roomtypes', RoomTypeViewSet, base_name='roomtypes')



urlpatterns = []
urlpatterns += nested_router.urls
urlpatterns += hotel_default_router.urls
urlpatterns += hotel_types_router.urls