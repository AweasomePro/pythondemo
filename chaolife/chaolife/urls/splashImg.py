from rest_framework import routers
from chaolife.views.splash import SplashViewSet
router = routers.SimpleRouter(trailing_slash=True)

router.register('^splash',SplashViewSet)

urlpatterns = []
urlpatterns += router.urls