from django.contrib.auth.models import update_last_login
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework import status

from ..helper.AppJsonResponse import DefaultJsonResponse
from ..serializers import UserSerializer
from ..helper.decorators import parameter_necessary
from django.contrib.auth.models import update_last_login
from django.utils.decorators import method_decorator
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
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

    @method_decorator(parameter_necessary('password','phoneNumber'))
    def post(self, request):
        print('CustomTokenAuthenticationView ,request.data is '+ str(request.data))
        print('CustomTokenAuthenticationView ,request.POST is '+str(request.POST))
        data = supportHumpField(request.data)
        print(data)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            update_last_login(None,user)
            token = serializer.object.get('token')
            token_data = jwt_response_payload_handler(token, user, request)
            userdata = UserSerializer(user, many=False).data
            json_response = DefaultJsonResponse(data={'user':userdata}, code=200, message="验证并登入成功")
            json_response['token'] = token_data['token']
            return json_response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


