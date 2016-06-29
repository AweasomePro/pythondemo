from rest_framework_nested import routers
from django.conf.urls import patterns, url
from rest_framework.routers import SimpleRouter

from hotelBooking.views.hotel import HouseViewSet


house_simple_router = SimpleRouter(trailing_slash=True,)
house_simple_router.register('house', HouseViewSet)
urlpatterns = []
urlpatterns += house_simple_router.urls