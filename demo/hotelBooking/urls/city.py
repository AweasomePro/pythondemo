from rest_framework_nested import routers
from django.conf.urls import patterns, url
from hotelBooking.views.city import CityViewSet
from .province import router as province_router

nested_router = routers.NestedSimpleRouter(province_router,r'province',lookup='province',trailing_slash=True)
nested_router.register(r'city',CityViewSet)

from rest_framework.routers import SimpleRouter
simpler_router = SimpleRouter()
simpler_router.register('city', CityViewSet)

urlpatterns = [

]
urlpatterns += simpler_router.urls
urlpatterns += nested_router.urls
