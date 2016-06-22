from django.conf.urls import patterns,url,include
from . import views

urlpatterns = [
    url(r'^login/$', views.member_login),
    url(r'^register/$', views.member_register),
    url(r'^ems/member/regist/$', views.member_resiter_sms_send),
    url(r'^installation/$', views.installationId_register),
    url(r'^installation/bind/$', views.installationId_bind),
    # url(r'^provinces/$', views.provinces),
    url(r'provinces',views.ProvinceView.as_view()),
    url(r'^hotel$',views.HotelView.as_view()),
    url(r'hotels$',views.HotelListView.as_view()),
    url(r'^avatar/token$', views.get_uploadAvatarToken),
]
