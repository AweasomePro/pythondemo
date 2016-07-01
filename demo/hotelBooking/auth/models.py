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

