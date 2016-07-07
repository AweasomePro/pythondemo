from django.conf.urls import include, url
from rest_framework import routers
from hotelBooking.urls import user,hotel,province,city,house,order
router = routers.SimpleRouter(trailing_slash=True)
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from hotelBooking.views import test
urlpatterns = [
    url(r'',include(user)),
    url(r'',include(hotel)),
    url(r'', include(province)),
    url(r'', include(city)),
    url(r'',include(house)),
    url(r'',include(order)),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'test',test.test)
]
urlpatterns += router.urls
