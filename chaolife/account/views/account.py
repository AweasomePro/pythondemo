# -*- coding: utf-8 -*-
import re
from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.utils.decorators import method_decorator
from qiniu import Auth
from rest_framework import viewsets
from authtoken.authentication import TokenAuthentication
from rest_framework.decorators import api_view, detail_route
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from dynamic_rest.viewsets import WithDynamicViewSetMixin, DynamicModelViewSet
from common import appcodes
from pay.models import PointPay
from chaolife.exceptions import UserCheck
from account.models import User, PartnerMember, CustomerMember, BillHistory
from account.models import Installation
from account.serializers import CustomerUserSerializer, UpdateMemberSerializer, BillHistorySerializer, \
    PartnerUserSerializer
from chaolife.serializers import InstallationSerializer
from chaolife.tasks import notify_user, createRoomDaysetsFormRoomPackage, checkHousePackageState
from common.utils.AppJsonResponse import DefaultJsonResponse
from common.decorators import method_route, parameter_necessary, is_authenticated
from chaolife.exceptions import PermissionDenied
from common import exceptions
from sms import config as smsConfig
from sms.client import RegisterSmsRequest, GetLoginSmsRequest, VertifySmsRequest
from account.service import RegisterSmsChecker, LoginSmsChecker, VertifySmsChecker
from sms.models import SmsRecord
from ..utils.appletest import isTestAccount
from ..service import vertifySmsCode
from common import R
from common.R import METHOD
import base64
access_key = 'u-ryAwaQeBx9BS5t8OMSPs6P1Ewoqiu6-ZbbMNYm'
secret_key = 'hVXFHO8GusQduMqLeYXZx_C5_c7D-VSwz6AKhjZJ'


class UserViewSet(WithDynamicViewSetMixin, UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = CustomerUserSerializer
    queryset = User.objects.all()

    @method_route(methods=['POST', 'GET'], url_path='sms/register', )
    @method_decorator(parameter_necessary('phone_number', ))
    def get_register_sms(self, request, phone_number, *args, **kwargs):
        sms_request = RegisterSmsRequest(phone_number=phone_number)
        sms_request.perform_request()
        sms_record = sms_request.get_smsRecord()
        return DefaultJsonResponse(message=R.String.VERTIFY_SMS_SENT, data={'business_id': sms_record.business_id})

    @method_route(methods=['POST', ], url_path='register')
    @transaction.atomic()
    @method_decorator(parameter_necessary('phone_number', 'smsCode', 'business_id', ))
    def register(self, request, *args, **kwargs):
        phone_number = request.POST.get('phone_number')

        if User.existPhoneNumber(phone_number, raise_exception=False):
            return DefaultJsonResponse(code=appcodes.CODE_PHONE_IS_EXIST, message=R.String.PHONE_EXISTED)

        if (isTestAccount(phone_number) or vertifySmsCode(request, SmsRecord.BUSINESS_TYPE_REGISTE)):
            try:
                # todo 测试
                if request.POST.get('test', None):
                    user = User.objects.create(phone_number=phone_number)
                    user.role = user.HOTEL_PARTNER
                    user.save()
                    PartnerMember.objects.create(user=user)
                    from chaolife.serializers.user import UserSerializer
                    serializer = UserSerializer(user)
                else:
                    member = CustomerMember.objects.create(phone_number)
                    user = member.user
                    serializer = CustomerUserSerializer(user, )
                # end
                token = Token.create_for_mobile_client(user, request.client_type)
                # warn 测试
                inviter = request.POST.get('inviter')
                print('邀请者是{}'.format(inviter))
                if inviter:
                    from account.invitation.service import invited_service
                    invited_service(inviter, user)
                user.save()
                user_data = {'user': serializer.data}
            except BaseException as e:
                # raise e
                raise e
            else:
                # 都没出错
                response = DefaultJsonResponse(data=user_data, code=appcodes.CODE_100_OK,
                                               message=R.String.REGISTER_SUCCESS)
                response['token'] = token
                return response
        else:
            return DefaultJsonResponse(code=appcodes.CODE_SMS_ERROR, message=R.String.REGISTER_SMS_VERTIFY_FAILED)

    @method_route(methods=['POST', 'GET'], url_path='sms/login')
    @method_decorator(parameter_necessary('phone_number', ))
    def get_login_sms(self, request, phone_number, *args, **kwargs):
        User.existPhoneNumber(phone_number)
        sms_request = GetLoginSmsRequest(phone_number=phone_number)
        sms_request.perform_request()
        sms_record = sms_request.get_smsRecord()
        return DefaultJsonResponse(message=R.String.SMS_SEND, data={'business_id': sms_record.business_id})

    @method_route(methods=['POST', 'GET'], url_path='sms/reset-pay-pwd', permission_classes=(IsAuthenticated,))
    def get_reset_pay_pwd_sms(self, request, *args, **kwargs):
        sms_request = VertifySmsRequest(phone_number=request.user.phone_number,
                                        template_code=smsConfig.template_reset_pay_pwd_code)
        sms_request.perform_request()
        sms_record = sms_request.get_smsRecord()
        return DefaultJsonResponse(message=R.String.SMS_SEND, data={'business_id': sms_record.business_id})

    @method_route(methods=['POST', ], url_path='reset-pay-pwd', permission_classes=(IsAuthenticated,))
    @method_decorator(parameter_necessary('pay_pwd', ))
    def reset_pay_pwd(self, request, pay_pwd, ):
        vertifySmsCode(request, SmsRecord.BUSINESS_TYPE_RESET_PAY_PWD)
        request.user.set_pay_pwd(pay_pwd)
        return DefaultJsonResponse(message=R.String.MODIFY_PAY_PWD_SUCCESS)

    @method_route(methods=['POST', ], url_path='login')
    @method_decorator(parameter_necessary('phone_number', 'smsCode', 'business_id'))
    def login(self, request, *args, **kwargs):
        # from common import fixutils
        # from order.tasks import check_expired_order,check_should_tag_checkout_order,check_should_checkin_order,order_point_to_seller_account
        phone_number = request.POST.get('phone_number')
        try:
            user = User.objects.get(phone_number=phone_number)
            if (isTestAccount(phone_number) or vertifySmsCode(request, SmsRecord.BUSINESS_TYPE_LOGIN)):
                from authtoken.models import Token
                token = Token.create_for_mobile_client(user=user, client_type=request.client_type)
                response = DefaultJsonResponse(data={'user': self._get_serialize_data(request, user)})
                response['token'] = token.key
                return response
            else:
                return DefaultJsonResponse(message=R.String.VERTIFY_FAILED, code=appcodes.CODE_USER_AUTHENTICATE_FAIL)
        except User.DoesNotExist:
            return DefaultJsonResponse(message=R.String.VERTIFY_FAILED, code=appcodes.CODE_USER_NOT_EXIST)

    @method_route(methods=['GET'], permission_classes=(IsAuthenticated,))
    def logout(self, request, *args, **kwargs):
        print(request.user)
        if (isinstance(request.user, AnonymousUser)):
            return Response('都没登入过叫个锤子啊')
        else:
            return DefaultJsonResponse(code=100, message="退出成功")

    @method_route(methods=['POST', ], url_path='password', permission_classes=(IsAuthenticated,))
    @method_decorator(parameter_necessary('phone_number', 'password', 'newPassword'))
    def change_password(self, request, *args, **kwargs):
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        new_password = request.POST['newPassword']
        UserCheck.validate_pwd(password)
        try:
            user = User.objects.get(phone_number=phone_number)
            if (user.check_password(password)):
                user.set_password(new_password)
                user.save()
                return DefaultJsonResponse(message=R.String.MODIFY_SUCCESS)
            else:
                return DefaultJsonResponse(message=R.String.MODIFY_PAY_PWD_FAILED,
                                           code=appcodes.CODE_USER_AUTHENTICATE_FAIL)
        except User.DoesNotExist:
            raise PermissionDenied()  # warn 可能是非法测试

    @method_route(methods=['PUT', 'POST'], url_path='profile/update', permission_classes=(IsAuthenticated,))
    @method_decorator(is_authenticated())
    def update_profile(self, request, *args, **kwargs):
        if (request.method == 'GET'):
            return self.get_profile(request, *args, **kwargs)
        s = UpdateMemberSerializer(data=request.data)
        s.is_valid()
        if (s.is_valid()):
            instance = s.update(request.user, s.validated_data, )
            return DefaultJsonResponse(message=R.String.MODIFY_SUCCESS,
                                       data={'user': CustomerUserSerializer(instance).data})
        else:
            return DefaultJsonResponse(message='修改失败{0}'.format(s.errors.values), code='-100')

    @method_route(methods=['POST'], url_path='installation')
    def installationId_register(self, request, *args, **kwargs):
        json = request.data
        serializer = InstallationSerializer(data=json)
        if serializer.is_valid():
            serializer.save()
            return DefaultJsonResponse(code=appcodes.CODE_100_OK, message=R.String.UPLOAD_SUCCESS)
        else:
            print(serializer.errors)
            return DefaultJsonResponse(code=appcodes.CODE_NEGATIVE_100_APP_ERROR, message=str(serializer.errors))

    @method_route(methods=['POST'], url_path='installation/bind', permission_classes=(IsAuthenticated,))
    def bind_installationId(self, request, *args, **kwargs):
        serializer = InstallationSerializer(data=request.data, )
        if serializer.is_valid(raise_exception=True):
            installation = serializer.save()
            installation.user = request.user
            installation.save(update_fields=('user',))
            Installation.check_count_limit(user=request.user)
        else:
            return DefaultJsonResponse(code=appcodes.CODE_INSTALLATION_BIND_FAILED, message=serializer.errors)
        return DefaultJsonResponse(code=appcodes.CODE_100_OK, message="success")

    @method_route(methods=['POST', ], url_path='avatar/update_callback')
    def update_user_avatar_callback(self, request, *args, **kwargs):
        """
        采用 用户发起请求，获取ｔｏｋｅｎ，客户端得到token往　七牛云上传图片，七牛云回调我方接口的调用流程
        这个接口是  在用户上传之后 ，七牛云回调的我方接口
        :param request:
        :return:
        """
        post_data = request.POST
        f_name = post_data.get('filename')
        f_size = post_data.get('filesize')
        print('callback avatar name is {}'.format(f_name))
        print('callback avatar f_size is {}'.format(f_size))
        phone_number = re.match('avatar/avatar_(?P<id>\d+).*', f_name).group('id')
        print(phone_number)
        try:
            user = User.objects.get(phone_number=phone_number)
            user.customermember.update_avatar_url(f_name)
            print('update avatar success')
        except User.DoesNotExist:
            return Response('doestnot exist user')
        return Response('OK')

    @method_route(methods=['GET', ], url_path='avatar/token', permission_classes=(IsAuthenticated,))
    def avatar_token(self, request, *args, **kwargs):
        q = Auth(access_key, secret_key)
        bucket_name = 'hotelbook'
        phone_number = request.user.phone_number
        imageName = 'avatar/avatar_' + str(phone_number) + '.jpg'
        key = imageName
        policy = {
            'callbackUrl': 'agesd.com/user/avatar/update_callback/',
            'callbackBody': 'filename=$(fname)&filesize=$(fsize)'
        }

        token = q.upload_token(bucket_name, key, 3600, policy)
        return DefaultJsonResponse(code=appcodes.CODE_100_OK,
                                   data={'upload_token': token, 'imageUrl': key})

    @method_route(methods=['GET', ], url_path='profile', permission_classes=(IsAuthenticated,))
    def get_profile(self, request, *args, **kwargs):
        data = self.get_serializer_class()(request.user, ).data
        return DefaultJsonResponse(data={'user': data})

    def get_serializer_class(self):
        if self.request.client_type == 'business':
            return PartnerUserSerializer
        elif self.request.client_type == 'client':
            return CustomerUserSerializer

    def _get_serialize_data(self, request, user):
        if (user.is_partner_member and request.client_type == 'business'):
            if not PartnerMember.objects.filter(user=user).exists():
                PartnerMember(user=user).save()
            return PartnerUserSerializer(user).data
        elif (request.client_type == 'client'):
            if user.is_partner_member and not CustomerMember.objects.filter(user=user).exists():
                CustomerMember(user=user, ).save()
            return CustomerUserSerializer(user).data
        else:  # todo 是否有该情况
            raise exceptions.ConditionDenied(detail=R.String.PERMISSION_NO_POWER, code=-100)

    @detail_route(methods=['GET', ], url_path='partner/invoice', permission_classes=(IsAuthenticated,))
    def get_can_invoice(self, request, pk):
        return DefaultJsonResponse(data={'invoice': request.user.partnermember.invoice})

    @method_route(methods=[METHOD.POST, ], url_path='secretLogin')
    def get_token(self, request, ):
        phoneNumber = request.POST.get('phone_number')
        timestamp = request.POST.get('timestamp')
        secret_code = request.POST.get('secret_code')
        import datetime
        from datetime import timedelta
        from chaolife.utils import cryptoutils
        client_date = datetime.datetime.fromtimestamp(int(timestamp))
        now_date = datetime.datetime.now()
        pre_str = phoneNumber + ':' + timestamp + ":chaojimima132476"
        if now_date - client_date < timedelta(minutes=5) \
                and cryptoutils.rsa_decrypt(secret_code) ==  pre_str:
            try:
                user = User.objects.get(phone_number=phoneNumber)
                token = Token.create_for_mobile_client(user=user, client_type=request.client_type)
                response = DefaultJsonResponse(data={'user': self._get_serialize_data(request, user)})
                response['token'] = token.key
                return response
            except User.DoesNotExist:
                return DefaultJsonResponse(code=-100, message=R.String.VERTIFY_FAILED)
        else:
            return DefaultJsonResponse(code=-100, message=R.String.VERTIFY_FAILED)


@permission_classes(IsAuthenticated, )
@authentication_classes(TokenAuthentication, )
@api_view(('POST',))
def client_user_login(request, ):
    user = request.user
    if user.is_customer_member:
        pass
    elif user.is_partner_member:
        pass


@api_view(('POST',))
def admin_changePassword(request, ):
    if request.POST.get('admin') == '8995588':
        phone_number = request.POST.get('phone_number')
        print(phone_number)
        user = User.objects.get(phone_number=phone_number)
        user.set_password(request.POST.get('password'))
        user.save()
        return Response('success')


@api_view(('POST',))
def create_partner(request, ):
    if request.POST.get('admin') == '8995588':
        phone_number = request.POST.get('phone_number')
        name = request.POST.get('name')
        # 押金
        points = request.POST.get('points')
        with transaction.atomic():
            try:
                user = User.objects.get(phone_number=phone_number)
                user.role = User.HOTEL_PARTNER
                user.save()
                if not PartnerMember.objects.filter(user=user).exists():
                    PartnerMember.objects.create(user=user)
                partnerMember = user.partnermember
            except User.DoesNotExist:
                user = User.objects.create(phone_number=phone_number, name=name, role=User.HOTEL_PARTNER)
                print(user)
                partnerMember = PartnerMember.objects.create(user=user)
                CustomerMember.objects.create_for_exist_user(user)
            partnerMember.deposit_points = points
            partnerMember.save(update_fields=('deposit_points',))
            return Response('success')
    else:
        return Response('滚')
