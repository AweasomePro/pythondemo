from django.conf.urls import patterns,url,include
from hotelBooking import views


urlpatterns = [
    url(r'^login/$', views.member_login),
    url(r'^register/$', views.member_register),
    url(r'^ems/member/regist/$', views.send_regist_sms),
    url(r'^installation/$',views.put_installtionId),
    url(r'installtion/bind/$',views.bindUserAndMobilePhone)
]
