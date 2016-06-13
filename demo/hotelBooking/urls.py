from django.conf.urls import patterns,url,include
from . import views

urlpatterns = [
    url(r'^login/$', views.member_login),
    url(r'^register/$', views.member_register),
    url(r'^ems/member/regist/$', views.member_resiter_sms_send),
    url(r'^installtion/$', views.installtionId_register),
    url(r'installtion/bind/$', views.installtionId_bind)
]
