from django.contrib.auth.decorators import login_required
from hotelBooking.core.order_creator.utils import add_hotel_order
from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from hotelBooking.core.models.products import Product
from hotelBooking import HousePackage
from hotelBooking.auth.decorators import login_required_and_is_member
from hotelBooking.serializers import HousePackageSerializer
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse


class HousePackageViewSet(viewsets.GenericViewSet):
    serializer_class = HousePackageSerializer
    queryset = HousePackage.objects.all()


def is_hotel_package(product):
    return product.name == '酒店套餐'


class HousePackageBookAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        return add_hotel_order(request)
        # print('print user')
        # self.is_member(request)
        # productId = request.POST.get('productId')
        # try:
        #     product = Product.objects.get(productId=productId)
        # except Product.DoesNotExist:
        #     return DefaultJsonResponse(res_data='不存在该商品',code=403)
        # # todo 判断是该类型的商品
        # is_hotel_package(product)
        # try:
        #     house_package = product.housepackage
        # except HousePackage.DoesNotExist:
        #     return DefaultJsonResponse(res_data='不存在该商品',code=403)
        # print('product id is {}'.format(productId))
        # return DefaultJsonResponse(res_data='订购成功')

    def is_member(self,request):
        if not request.user.is_customer_member:
            return DefaultJsonResponse(res_data='你还不是会员',code=-100)

    def point_is_match(self,user):
        if (user.point < 10):
            pass


