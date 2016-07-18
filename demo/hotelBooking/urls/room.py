from rest_framework_nested import routers
from django.conf.urls import patterns, url
from rest_framework.routers import SimpleRouter

from hotelBooking.views.hotel import RoomViewSet


room_simple_router = SimpleRouter(trailing_slash=False, )
room_simple_router.register('^room', RoomViewSet)
urlpatterns = []
urlpatterns += room_simple_router.urls