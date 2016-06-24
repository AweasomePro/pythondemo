from django.conf.urls import patterns,url,include
from . import views
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from .auth.models import CustomTokenAuthenticationView


router = routers.SimpleRouter()
router.register(r'provinces',views.ProvinceView)
router.register(r'hotels')
router.register(r'user',views.UserViewSet)
urlpatterns = [
    # url(r'^login/$', views.member_login),
    # url(r'^register/$', views.member_register),
    url(r'^ems/member/regist/$', views.member_resiter_sms_send),
    url(r'^installation/$', views.installationId_register),
    # url(r'^installation/bind/$', views.installationId_bind),
    # url(r'^provinces/$', views.provinces),
    # url(r'provinces',views.ProvinceView.as_view()),
    url(r'^hotel$',views.HotelView.as_view()),
    url(r'hotels$',views.HotelListView.as_view()),
    url(r'^avatar/token$', views.obtain_uploadAvatarToken),
    url(r'^avatar/upload/callback', views.update_user_avatar_callback),
    url(r'^api-token-auth/', CustomTokenAuthenticationView.as_view()),
    url(r'^user/login/', CustomTokenAuthenticationView.as_view()),

]

urlpatterns += router.urls

