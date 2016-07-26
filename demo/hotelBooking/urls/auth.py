from django.conf.urls import url
from hotelBooking.authtoken import views
urlpatterns = []
urlpatterns += [
    url(r'^api-token-auth/', views.ObtainAuthToken.as_view()),
    url(r'^api-token-verify/', views.VerifyWebToken.as_view()),
]