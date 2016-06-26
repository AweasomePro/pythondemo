from django.conf.urls import patterns,url,include
from . import views
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from .auth.models import CustomTokenAuthenticationView


router = routers.SimpleRouter(trailing_slash=True)
router.register(r'hotel',views.HotelViewSet)
router.register(r'user',views.UserViewSet)
urlpatterns = [
    url(r'^ems/member/regist/$', views.member_resiter_sms_send),
    url(r'^installation/$', views.installationId_register),
    url(r'provinces',views.ProvinceView.as_view()),
    # url(r'^hotel$',views.HotelView.as_view()),
    # url(r'hotels$',views.HotelListView.as_view()),
    url(r'^avatar/upload/callback', views.update_user_avatar_callback),
    url(r'^api-token-auth/', CustomTokenAuthenticationView.as_view()),
    url(r'^user/login/', CustomTokenAuthenticationView.as_view()),

]

urlpatterns += router.urls

