from django.conf.urls import include, url
from rest_framework import routers
from hotelBooking.urls import user,hotel,province,city,room,order,product,pay,auth
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from hotelBooking.views import test
from hotelBooking.views.sms import SmsAPIView
router = routers.SimpleRouter(trailing_slash=True)

urlpatterns = [
    url(r'^sms/',SmsAPIView.as_view()),
    url(r'',include(user)),
    url(r'',include(hotel)),
    url(r'', include(province)),
    url(r'', include(city)),
    url(r'', include(room)),
    url(r'',include(order)),
    url(r'',include(product)),
    url(r'', include(pay)),
    url(r'',include(auth)),
    url(r'^test/$',test.test),
    url(r'^init',test.init),
]
urlpatterns += router.urls

