from rest_framework_nested import routers
from django.conf.urls import patterns, url
from hotelBooking.views.city import CityViewSet
from .province import router as province_router
nested_router = routers.NestedSimpleRouter(province_router,r'province',lookup='province',trailing_slash=True)
nested_router.register(r'city',CityViewSet)
urlpatterns = [

]
urlpatterns += nested_router.urls