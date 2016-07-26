import re

from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.utils.decorators import method_decorator
from qiniu import Auth
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from hotelBooking import appcodes
from hotelBooking.core.utils.serializer_helpers import wrapper_response_dict
from hotelBooking.exceptions import  UserCheck
from hotelBooking.models import User,PartnerMember,CustomerMember
from hotelBooking.models.installation import Installation
from hotelBooking.module import sms
from hotelBooking.serializers import CustomerUserSerializer, UpdateMemberSerializer
from hotelBooking.serializers import InstallationSerializer
from hotelBooking.serializers.user import UserSerializer
from hotelBooking.tasks import simple_notify,send_sms
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse
from hotelBooking.utils.decorators import method_route, parameter_necessary, is_authenticated



access_key = 'u-ryAwaQeBx9BS5t8OMSPs6P1Ewoqiu6-ZbbMNYm'
secret_key = 'hVXFHO8GusQduMqLeYXZx_C5_c7D-VSwz6AKhjZJ'


class UserViewSet(UpdateModelMixin,viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    # permission_classes = (login_required,)
    serializer_class = CustomerUserSerializer
    queryset = User.objects.all()

    @method_route(methods=['POST', 'GET'], url_path='sms/register')
    @method_decorator(parameter_necessary('phoneNumber', ))
    def get_register_sms(self, request, phoneNumber, *args, **kwargs):
        if not User.existPhoneNumber(phoneNumber,raise_exception=False):
            response = send_sms.delay(phoneNumber, template='register')
            return Response(wrapper_response_dict(message='验证码已发送'))
        else:
            return Response(wrapper_response_dict(message='手机号已存在',code=-100))

    @method_route(methods=['POST',],url_path='register')
    @transaction.atomic()
    @method_decorator(parameter_necessary('phoneNumber', 'smsCode',))
    def register(self, request, *args, **kwargs):
        phone_number = request.POST.get('phoneNumber')
        password = request.POST.get('smsCode')
        sms_code = request.POST.get('smsCode', None)
        print(sms_code)
        if User.existPhoneNumber(phone_number,raise_exception=False):
            return DefaultJsonResponse(code=appcodes.CODE_SMS_ERROR, message="手机号已存在")
        # UserCheck.validate_pwd(password)
        if (sms.verify_sms_code(phone_number,sms_code)[0] or True):
            try:
                # todo 测试
                if request.POST.get('test',None):
                    user =User.objects.create(phone_number = phone_number)
                    user.set_password(password)
                    user.role = user.HOTEL_PARTNER
                    user.save()
                    parter = PartnerMember.objects.create(user = user)
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    res = {'token': token}
                    return Response(data=res)
                else:
                    member = CustomerMember.objects.create(phone_number, password)
                    assert  member.user.check_password(raw_password=password) == True
                # end
                serializer_member = CustomerUserSerializer(member.user, )
                payload = jwt_payload_handler(member.user)
                token = jwt_encode_handler(payload)
                kwargs = {'user': serializer_member.data}
            except BaseException as e:
                # raise e
                raise e
            else:
                response = DefaultJsonResponse(res_data= kwargs, code=appcodes.CODE_100_OK, message="注册成功")
                response['token'] = token
                return response
        else:
            return DefaultJsonResponse(code=appcodes.CODE_SMS_ERROR, message="注册失败，验证码错误")

    @method_route(methods=['POST', 'GET'], url_path='sms/login')
    @method_decorator(parameter_necessary('phoneNumber',))
    def get_login_sms(self,request,phoneNumber,*args,**kwargs):
        User.existPhoneNumber(phoneNumber)
        response = send_sms.delay(phoneNumber,template='login')
        return Response(wrapper_response_dict(message='验证码已发送'))


    @method_route(methods=['POST',], url_path='login')
    @method_decorator(parameter_necessary('phoneNumber',))
    def login(self, request, *args, **kwargs):
        print(request.version)
        # checkHousePackageState()
        phone_number = request.POST.get('phoneNumber')
        password = request.POST.get('password',None)
        smsCode = request.POST.get('smsCode',None)
        print('phone is {}'.format(phone_number))
        try:
            user = User.objects.get(phone_number=phone_number)
            if ( True or smsCode and user.check_smscode(phone_number,smsCode) ):
                from rest_framework.authtoken.models import Token
                token,create = Token.objects.get_or_create(user=user)
                if(user.role == User.CUSTOMER):
                    response = DefaultJsonResponse(res_data={'user':CustomerUserSerializer(user).data})
                else:
                    response = DefaultJsonResponse(res_data={'user':UserSerializer(user).data})
                response['token'] = token.key
                simple_notify.delay(user.phone_number,message='登入成功')
                return response
            else:
                return DefaultJsonResponse(message='验证失败',code=-100)
        except User.DoesNotExist:
            return DefaultJsonResponse(message='验证失败,不存在该账号', code=-100)

    @method_route(methods=['POST'],)
    @method_decorator(is_authenticated())
    def logout(self,request, *args, **kwargs):
        print(request.user)
        if(isinstance(request.user,AnonymousUser)):
            return Response('都没登入过叫个锤子啊')
        else:
            return DefaultJsonResponse(code=100,message="退出成功")

    @method_route(methods=['POST',], url_path='password')
    @method_decorator(parameter_necessary('phoneNumber', 'password', 'newPassword'))
    def change_password(self,request, *args, **kwargs):
        phoneNumber = request.POST['phoneNumber']
        password = request.POST['password']
        new_password = request.POST['newPassword']
        UserCheck.validate_pwd(password)
        try:
            user = User.objects.get(phone_number=phoneNumber)
            if (user.check_password(password)):
                user.set_password(new_password)
                user.save()
                return DefaultJsonResponse(message='修改成功')
            else:
                return DefaultJsonResponse(message='修改失败,密码错误')
        except User.DoesNotExist:
            return DefaultJsonResponse(message='用户不存在，修改失败')

    @method_route(methods=['PUT'],url_path='profile')
    @method_decorator(is_authenticated())
    def update_profile(self,request, *args, **kwargs):
        print(request.user)
        print(request.data)
        s = UpdateMemberSerializer(data=request.data)
        s.is_valid()
        print(s.errors)
        if(s.is_valid()):
            instance = s.update(request.user,s.validated_data,)
            return DefaultJsonResponse(message='修改用户资料成功', res_data={'user':CustomerUserSerializer(instance).data})
        else:
            return DefaultJsonResponse(message='修改失败{0}'.format(s.errors.values),code='-100')

    @method_route(methods=['POST'], url_path='installation')
    def installationId_register(self,request,  *args, **kwargs):
        json = request.data
        print(str(json))
        serializer = InstallationSerializer(data=json)
        # androidDevice = Installation.objects.get(installationId=installationId)
        # iosDevice = Installation.objects.get(deviceToken=installationId)
        if serializer.is_valid():
            deviceType  = serializer.initial_data.get('deviceType')
            is_uploaded = False
            if (deviceType == 'android' and Installation.objects.filter(installationId=serializer.initial_data.get('installationId',None)).exists())\
                or (deviceType =='ios') and Installation.objects.filter(deviceToken=serializer.initial_data.get('deviceToken',None)).exists():
                return Response(wrapper_response_dict(message='已经上传过了'))
            serializer.save()
            return DefaultJsonResponse(code=appcodes.CODE_100_OK, message="上传成功")
        else:
            print(serializer.errors)
            return DefaultJsonResponse(code=appcodes.CODE_NEGATIVE_100_APP_ERROR, message=str(serializer.errors))

    @method_route(methods=['POST'], url_path='installation/bind')
    @method_decorator(is_authenticated())
    def bind_installationId(self,request, *args, **kwargs):
        phoneNumber = request.user.phone_number
        installationId = request.POST.get('installationId')
        deviceToken = request.POST.get('deviceToken')
        user = None
        if installationId:
            try:
                installDevice = Installation.objects.get(installationId=installationId)
            except Installation.DoesNotExist:
                return DefaultJsonResponse(code=appcodes.CODE_INSTALLATION_BIND＿FAILED_NOT_UPLOADED, message="installationId尚未注册到服务端")
        elif deviceToken:
            try:
                installDevice = Installation.objects.get(deviceToken=deviceToken)
            except Installation.DoesNotExist:
                return DefaultJsonResponse(code=appcodes.CODE_INSTALLATION_BIND＿FAILED_NOT_UPLOADED,
                                           message="installationId尚未注册到服务端")
        else:
            raise ValidationError(detail='参数错误',)
        user = User.objects.get(phone_number=phoneNumber)

        if(user.installation_set.all().count()!=0):
            user.installation_set.all().delete()

        installDevice.user = user
        installDevice.save()
        return DefaultJsonResponse(code=appcodes.CODE_100_OK, message="success")

    @method_route(methods=['POST',], url_path='avatar/update_callback')
    def update_user_avatar_callback(self,request, *args, **kwargs):
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
            user = User.objects.get(phone_number = phone_number)
            user.customermember.update_avatar_url(f_name)
            print('update avatar success')
        except User.DoesNotExist:
            return Response('doestnot exist user')
        return Response('OK')

    @method_route(methods=['GET',],url_path='avatar/token')
    @method_decorator(is_authenticated())
    def avatar_token(self,request, *args, **kwargs):
        q = Auth(access_key, secret_key)
        bucket_name = 'hotelbook'
        phone_number = request.user.phone_number
        imageName = 'avatar/avatar_' + str(phone_number) + '.jpg'
        key = imageName
        policy = {
            'callbackUrl':'agesd.com/user/avatar/update_callback/',
            'callbackBody':'filename=$(fname)&filesize=$(fsize)'
        }

        token = q.upload_token(bucket_name, key, 3600,policy)
        return DefaultJsonResponse(code=appcodes.CODE_100_OK,
                                   res_data={'upload_token': token, 'imageUrl': key})

    def get_serializer_class(self):
        if(self.request.user.is_partner_member):
            return UserSerializer
        elif(self.request.user.is_customer_member):
            return CustomerUserSerializer
        else: #todo 是否有该情况
            return self.serializer_class