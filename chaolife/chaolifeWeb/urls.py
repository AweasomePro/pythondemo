# -*- coding:utf-8 -*-
from rest_framework import routers
from django.conf.urls import url
from . import views
from chaolifeWeb.feedback import views as feedback_views
router = routers.SimpleRouter()
router.register(r'^feedback',feedback_views.FeedbackView)

urlpatterns = [
    url('^$',views.home),
    url('^booking-terms',views.booking_terms),
    url('^user-service-terms',views.user_service_terms),
    url('^now',views.time_now)

]
urlpatterns += router.urls
