from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from hotelBooking import HousePackage
from hotelBooking.auth.decorators import login_required_and_is_member
from hotelBooking.serializers import HousePackageSerializer
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse


class HousePackageViewSet(viewsets.GenericViewSet):
    serializer_class = HousePackageSerializer
    queryset = HousePackage.objects.all()

@api_view(['POST',])
@authentication_classes((JSONWebTokenAuthentication,))
@login_required_and_is_member()
def book_house_package(request,):
    print(request.user)
    return DefaultJsonResponse(res_data='订购成功')


