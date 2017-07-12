from django.conf.urls import include, url
from rest_framework import routers
from chaolife.urls import hotel,province,city,room,order,product,splashImg,shaernotify
from chaolife.views import test
router = routers.SimpleRouter(trailing_slash=True)

urlpatterns = [
    url(r'',include(hotel)),
    url(r'', include(province)),
    url(r'', include(city)),
    url(r'', include(room)),
    url(r'',include(order)),
    url(r'',include(product)),
    url(r'',include(splashImg)),
    url(r'^test/$',test.test),
    url(r'^init',test.init),
    url(r'',include(shaernotify)),
]
urlpatterns += router.urls

