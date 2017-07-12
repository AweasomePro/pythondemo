from rest_framework import routers
from . import views as user_view
from django.conf.urls import url

from account.authtoken import views as auth_views
router = routers.SimpleRouter(trailing_slash=True)
router.register(r'user', user_view.UserViewSet)
router.register(r'billhistory',user_view.BillHistoryView)
router.register(r'pointredemption',user_view.PointRedemptionsViewSet)
urlpatterns = [
    url(r'^api-token-auth/', auth_views.ObtainAuthToken.as_view()),
    url(r'^api-token-verify/', auth_views.VerifyWebToken.as_view()),
    url(r'xadmin/admin/cpwd/',user_view.admin_changePassword),
    url(r'xadmin/admin/create_partner/',user_view.create_partner),

]
urlpatterns += router.urls