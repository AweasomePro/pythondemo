from django.conf.urls import patterns, url, include

from .views import ApkViewSets
from rest_framework import routers
router = routers.SimpleRouter(trailing_slash=True)
router.register(r'apk', ApkViewSets)
urlpatterns = [

]
urlpatterns += router.urls
