from django.shortcuts import render

# Create your views here.
from common.viewsets import CustomDynamicModelViewSet
from .serializers import SmsRecordSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
# class GetSmsViewSet(CustomDynamicModelViewSet):
#     serializer_class =
from sms.client import VertifySmsRequest
from sms import config as smsConfig

TYPE_REGISTER = 'register'
TYPE_LOGIN = 'login'
TYPE_RESET_PAY_PWD = 'reset-pay-pwd'

ALLOW_SMS_TYPE =(TYPE_REGISTER,TYPE_LOGIN,TYPE_RESET_PAY_PWD)

@api_view(('GET',))
@permission_classes((IsAuthenticated,))
def require_vertify_sms(request):
    type = request.GET.get('type')
    user = request.user
    VertifySmsRequest(user.phone_number,template_code=smsConfig.template_reset_pay_pwd_code).perform_request()
