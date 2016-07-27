from rest_framework import routers
from django.conf.urls import patterns, url
from rest_framework_jwt.views import obtain_jwt_token
from hotelBooking.views import user as user_view
router = routers.SimpleRouter(trailing_slash=True)
router.register(r'user', user_view.UserViewSet,)
urlpatterns = [
    url(r'^api-token-auth/', obtain_jwt_token),
]
urlpatterns += router.urls