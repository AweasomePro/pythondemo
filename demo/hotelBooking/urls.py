from django.conf.urls import patterns,url,include
from hotelBooking import views


urlpatterns = [
    url(r'^login$', views.member_login),
    url(r'^register$', views.member_register),
]
