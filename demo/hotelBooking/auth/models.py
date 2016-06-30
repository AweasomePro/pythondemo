from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import ugettext as _
from hotelBooking.models import User
from ..utils.AppJsonResponse import DefaultJsonResponse
from ..serializers import CustomerMemberSerializer
from ..utils.decorators import parameter_necessary
from .. import appcodes
from django.contrib.auth.models import update_last_login
from django.utils.decorators import method_decorator
from rest_framework import serializers
from rest_framework_jwt.utils import jwt_payload_handler
from hotelBookingProject import settings
import jwt
def create_token(user):
    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, settings.SECRET_KEY)
    return token.decode('unicode_escape')

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


def supportHumpField(data):
    """
    适配 客户端请求的接口
    :param data:
    :return:
    """
    if 'phoneNumber' in data:
        copy_data = data.copy()
        copy_data['phone_number'] = copy_data['phoneNumber']
        print(copy_data)
        copy_data.pop('phoneNumber')
        print('做了修改')
        print(copy_data)
        return copy_data

class CustomTokenAuthenticationView(ObtainJSONWebToken):
    """Implementation of ObtainAuthToken with last_login update"""
    # serializer_class = LoginAuthenSeraializer
    # serializer_class = LoginAuthenSeraializer

    @method_decorator(parameter_necessary('password','phoneNumber'))
    def post(self, request, *args, **kwargs):
        data = supportHumpField(request.data)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            update_last_login(None,user)
            member = CustomerMemberSerializer(user.customermember)
            response = DefaultJsonResponse(res_data={'member':member.data})
            response['token'] = token
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)