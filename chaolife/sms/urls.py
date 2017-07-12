from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import require_vertify_sms
pay_router = DefaultRouter()
urlpatterns = [
    url(r'^sms/',require_vertify_sms)
]
urlpatterns += pay_router.urls
