from django.conf.urls import include, url
from rest_framework import routers

from hotelBooking.auth.models import CustomTokenAuthenticationView
from . import user,hotel,province,city
router = routers.SimpleRouter(trailing_slash=True)

urlpatterns = [
    url(r'',include(user)),
    url(r'',include(hotel)),
    url(r'', include(province)),
    url(r'', include(city))
]
urlpatterns += router.urls
