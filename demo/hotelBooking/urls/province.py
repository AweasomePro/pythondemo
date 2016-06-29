from rest_framework_nested import routers
from django.conf.urls import patterns, url
from hotelBooking.views.province import ProvinceViewSet
router = routers.DefaultRouter(trailing_slash=True,)
router.register(r'province',ProvinceViewSet,base_name='province')
# city_router = routers.NestedSimpleRouter(nested_router,r'city',lookup='city')
# city_router.register(r'')
urlpatterns = [

]
urlpatterns += router.urls