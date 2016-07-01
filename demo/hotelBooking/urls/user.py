from rest_framework import routers
from django.conf.urls import patterns, url

from hotelBooking.auth.models import CustomTokenAuthenticationView
from rest_framework_jwt.views import JSONWebTokenAPIView
from hotelBooking.views import user as user_view
router = routers.SimpleRouter(trailing_slash=True)
router.register(r'user', user_view.UserViewSet)
urlpatterns = [
    url(r'^user/login$', CustomTokenAuthenticationView.as_view()),]
urlpatterns += router.urls