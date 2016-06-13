from django.conf.urls import patterns,url,include
from . import views

urlpatterns = [
    url(r'^login/$', views.member_login),
    url(r'^register/$', views.member_register),
    url(r'^ems/member/regist/$', views.member_resiter_sms_send),
    url(r'^installation/$', views.installationId_register),
    url(r'installation/bind/$', views.installationId_bind)
]
