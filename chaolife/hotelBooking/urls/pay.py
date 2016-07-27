from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from hotelBooking.views.pay import client
pay_router = DefaultRouter()
urlpatterns = [
    url(r'^point/pay/$', client.PointPayView.as_view()),
    url(r'^alipay/notify/$', client.alipay_notify)
]
