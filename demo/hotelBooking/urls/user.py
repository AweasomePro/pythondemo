from rest_framework import routers
from django.conf.urls import patterns, url

from hotelBooking.auth.models import CustomTokenAuthenticationView
from hotelBooking.views import user
router = routers.SimpleRouter(trailing_slash=True)
router.register(r'user',user.UserViewSet)
urlpatterns = [
    url(r'^user/login/', CustomTokenAuthenticationView.as_view()),]
urlpatterns += router.urls