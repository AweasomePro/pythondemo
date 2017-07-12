from rest_framework import routers
from chaolife.views.sharenotify import ShareNotifyViewSet
router = routers.SimpleRouter(trailing_slash=True)

router.register('^share-notify',ShareNotifyViewSet)

urlpatterns = []
urlpatterns += router.urls