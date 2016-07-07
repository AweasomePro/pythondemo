from django.contrib.auth.models import AnonymousUser
from django.db.models import Model
import requests
from django.utils.decorators import method_decorator
from hotelBooking.core.exceptions import  UserCheck
from hotelBooking.core.serializers.user import UserSerializer, UpdateMemberSerializer
from qiniu import Auth
from rest_framework.authentication import BasicAuthentication
from rest_framework.mixins import UpdateModelMixin
from rest_framework import viewsets
from rest_framework.response import Response
from hotelBooking.Mysettings import APP_ID, APP_KEY
from hotelBooking.serializers import  UpdateCustomerMemberSerializer, InstallationSerializer
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse
from hotelBooking.utils.decorators import method_route, parameter_necessary, is_authenticated
from hotelBooking import User
import re
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from . import appcodes,Installation,CustomerMember
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER






access_key = 'u-ryAwaQeBx9BS5t8OMSPs6P1Ewoqiu6-ZbbMNYm'
secret_key = 'hVXFHO8GusQduMqLeYXZx_C5_c7D-VSwz6AKhjZJ'


def verifySmsCode(mobilePhoneNumber, smscode):
    url = 'https://api.leancloud.cn/1.1/verifySmsCode/' + str(smscode)
    print(url)
    values = {
        "mobilePhoneNumber": str(mobilePhoneNumber),
    }
    headers = {'X-LC-Id': APP_ID, 'X-LC-Key': APP_KEY, 'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, params=values)
    response.encoding = 'utf-8'
    # 使用异步
    print(response.content)
    print(response.status_code)
    print(type(response.json()))
    if response.status_code == 200:
        return True, "Success"
    elif response.json().get('code', 0) == 603:
        # Invalid SMS code
        print(response.json()['code'])
        return False, "Invalid SMS code"
    else:
        return False, "尚未处理的错误"

class UserViewSet(UpdateModelMixin,viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, BasicAuthentication)

    serializer_class = UserSerializer
    queryset = User.objects.all()

    @method_route(methods=['POST'],url_path='register')
    @method_decorator(parameter_necessary('phoneNumber', 'password', 'smsCode',))
    def register(self, request):
        phone_number = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        sms_code = request.POST.get('smsCode', None)
        print(sms_code)
        if (not User.existPhoneNumber(phone_number=phone_number)):
            UserCheck.validate_pwd(password)
            if sms_code != None:
                # verifySuccess, message = verifySmsCode(phone_number, password)
                if (True):
                    try:
                        member = CustomerMember.objects.create(phone_number,password)
                        print('member 的phoneNumber' + str(member.user.phone_number))
                        print('member name =' + str(member.user.name))
                        serializer_member = UserSerializer(member.user,exclude_fields=('password',))
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
        else:
            return DefaultJsonResponse(code=appcodes.CODE_PHONE_IS_EXISTED, message="手机号已经存在")

    @method_route(methods=['POST'], url_path='login')
    @method_decorator(parameter_necessary('phoneNumber', 'password', ))
    def login(self, request):
        phone_number = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        try:
            user = User.objects.get(phone_number=phone_number)
            if (user is not None and user.check_password(password)):
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = DefaultJsonResponse(res_data={'user':UserSerializer(user).data})
                response['token'] = token
                return response
            else:
                return DefaultJsonResponse(message='验证失败',code=-100)
        except User.DoesNotExist:
            return DefaultJsonResponse(message='验证失败,不存在该账号', code=-100)

    @method_route(methods=['POST'],)
    @method_decorator(is_authenticated())
    def logout(self,request):
        print(request.user)
        if(isinstance(request.user,AnonymousUser)):
            return Response('都没登入过叫个锤子啊')
        else:
            return DefaultJsonResponse(code=100,message="退出成功")

    @method_route(methods=['PUT'], url_path='password')
    @method_decorator(parameter_necessary('phoneNumber', 'password', ))
    def change_password(self,request):
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
    def update_profile(self,request):
        print(request.user)
        print(request.data)
        s = UpdateMemberSerializer(data=request.data)
        s.is_valid()
        print(s.errors)
        if(s.is_valid()):
            instance = s.update(request.user,s.validated_data,)
            return DefaultJsonResponse(message='修改用户资料成功',res_data={'user':UserSerializer(instance).data})
        else:
            return DefaultJsonResponse(message='修改失败{0}'.format(s.errors.values),code='-100')



    @method_route(methods=['POST'], url_path='installation')
    def installationId_register(self,request, formate=None):
        json = request.data
        print(str(json))
        serializer = InstallationSerializer(data=json)
        if serializer.is_valid():
            print('valid' + serializer.__str__())
            serializer.save()
            return DefaultJsonResponse(code=appcodes.CODE_100_OK, message="上传成功")
        else:
            print(serializer.errors)
            return DefaultJsonResponse(code=appcodes.CODE_NEGATIVE_100_APP_ERROR, message=str(serializer.errors))

    @method_route(methods=['POST'], url_path='installation/bind')
    @method_decorator(is_authenticated())
    def bind_installationId(self,request):
        phoneNumber = request.user.pk
        installationId = request.POST.get('installationId')
        deviceToken = request.POST.get('deviceToken')
        if installationId:
            try:
                installDevice = Installation.objects.get(installationId=installationId)
                user = User.objects.get(phone_number=phoneNumber)
                installDevice.member = user
                installDevice.save()
                return DefaultJsonResponse(code=appcodes.CODE_100_OK, message="success")
            except Installation.DoesNotExist:
                return DefaultJsonResponse(code=appcodes.CODE_INSTALLATION_BIND＿FAILED_NOT_UPLOADED, message="这个installationId尚未注册到服务端")
        elif deviceToken:
            return DefaultJsonResponse(code=appcodes.CODE_100_OK, message="ios还没写,哇咔咔")

    @method_route(methods=['POST'], url_path='avatar/update_callback')
    def update_user_avatar_callback(self,request):
        """
        采用 用户发起请求，获取ｔｏｋｅｎ，客户端得到token往　七牛云上传图片，七牛云回调我方接口的调用流程
        这个接口是  在用户上传之后 ，七牛云回调的我方接口
        :param request:
        :return:
        """
        post_data = request.POST
        f_name = post_data.get('filename')
        f_size = post_data.get('filesize')
        print(type(re.match('^avatar_(?P<id>\d+).*', f_name)))
        try:
            phone_number = re.match('^avatar_(?P<id>\d+).*', f_name).group('id')
            if (phone_number and User.existPhoneNumber(phone_number=phone_number)):
                CustomerMember.update_user_avatar(phone_number,f_name)
                print('update avatar success')
            else:
                print('update avatar error')
        except BaseException as e:
            print('发生异常了')
            print(e.__traceback__)
        return Response('OK')

    @method_route(methods=['GET',],url_path='avatar/token')
    @method_decorator(is_authenticated())
    def avatar_token(self,request):
        q = Auth(access_key, secret_key)
        bucket_name = 'hotelbook'
        phone_number = request.user.phone_number
        imageName = '/avatar/avatar_' + str(phone_number) + '.jpg'
        key = imageName
        policy = {
            'callbackUrl':'agesd.com/avatar/update_callback',
            'callbackBody':'filename=$(fname)&filesize=$(fsize)'
        }
        token = q.upload_token(bucket_name, key, 3600,policy)
        return DefaultJsonResponse(code=appcodes.CODE_100_OK,
                                   res_data={'upload_token': token, 'imageUrl': key})

