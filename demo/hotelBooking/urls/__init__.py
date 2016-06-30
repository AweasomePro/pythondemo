from django.conf.urls import include, url
from rest_framework import routers

from hotelBooking.auth.models import CustomTokenAuthenticationView
from . import user,hotel,province,city,house
router = routers.SimpleRouter(trailing_slash=True)
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = [
    url(r'',include(user)),
    url(r'',include(hotel)),
    url(r'', include(province)),
    url(r'', include(city)),
    url(r'',include(house)),
]
urlpatterns += router.urls
