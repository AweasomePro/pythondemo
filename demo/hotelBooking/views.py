#-*-coding:utf-8-*-
import requests
import json
from .helper import modelKey
from .helper.decorators import parameter_necessary
from .helper.AppJsonResponse import JSONWrappedResponse,DefaultJsonResponse
from .models import *
from .serializers import *
from .helper import userhelper
import logging

# from rest_framework.renderers import JSONRenderer

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib import auth
from django.contrib.sessions.models import Session, SessionManager
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.dispatch import receiver
from django.core.paginator import Paginator,EmptyPage
from django.conf import settings
from django.db.models.signals import post_save

from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes,permission_classes,authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication,TokenAuthentication

from qiniu import Auth

logger = logging.getLogger(__name__)

APP_ID = "P0fN7ArvLMtcgsACRwhOupHj-gzGzoHsz"
APP_KEY = "cWK8NHllNg7N6huHiKA1HeRG"

callback_url = ''


class AppConst:
    STATUS_SUCCESSS = '100'
    STATUS_ERROR = '-100'
    STATUS_PWD_ERROR = '102'
    STATUS_PHONE_EXISTED = '103'
    STATUS_PHONE_NOT_EXISTED = '104'


@never_cache
@parameter_necessary('phoneNumber', 'password', )
def member_login(request):
    phoneNumber = request.POST.get(modelKey.KEY_PHONENUMBER)
    password = request.POST.get('password')
    try:
        user = User.objects.get(phone_number=phoneNumber)
        valid = user.check_password(password)
        if valid and user.is_active:
            # auth.login(request,user)
            print('login user ' + str(user.phone_number))
            kwargs = {'UserEntity': UserSerializer(user, many=False).data}
            response = JSONWrappedResponse(data=kwargs, status=AppConst.STATUS_SUCCESSS, message="登入成功")
            print('settings session cookie name is :' + settings.SESSION_COOKIE_NAME)
            return response
        else:
            return JSONWrappedResponse(status=AppConst.STATUS_PWD_ERROR, message="账号密码错误", )
    except User.DoesNotExist:
        return JSONWrappedResponse(status=AppConst.STATUS_PHONE_NOT_EXISTED, message="不存在该账号")
    except Exception as e:
        print('exception ' + e.__str__())
        return JSONWrappedResponse(status=401, message="服务器内部请求错误")


@never_cache
@csrf_exempt
@api_view(['POST'])
@parameter_necessary('phoneNumber', 'password', 'smsCode')
def member_register(request):
    phone_number = request.POST.get('phoneNumber')
    password = request.POST.get('password')
    sms_code = request.POST.get('smsCode', None)
    print(sms_code)
    if (not userhelper.phoneNumberExist(phone_number)):
        if sms_code != None:
            # verifySuccess, message = verifySmsCode(phone_number, password)
            if (True):
                try:
                    user = User()
                    print('user 的phoneNumber' + str(user.phone_number))
                    user.phone_number = phone_number
                    user.set_password(password)
                    user.username = phone_number
                    print('user 的username =' + str(user.username))
                    # token = Token.objects.create(user=user)
                    serailizer_member = UserSerializer(user, many=False)
                    # serailizer_member.data
                    kwargs = {'UserEntity': serailizer_member.data}
                    user.save()
                    token = Token.objects.get(user_id=user.id)
                    print('token is {}'.format_map(token.id))
                    # response = {'token':token}
                    # print(type(response))
                    # return JSONWrappedResponse(response)
                    # return Response({'token':str(token)})
                except BaseException as e:
                    raise e
                    return DefaultJsonResponse(data=kwargs, status=AppConst.STATUS_ERROR, message="内部错误")
                else:
                    return DefaultJsonResponse(data=kwargs, status=AppConst.STATUS_SUCCESSS, message="注册成功",token=token)
            else:
                return JSONWrappedResponse(status=AppConst.STATUS_PWD_ERROR, message="注册失败，验证码错误")
    else:
        return JSONWrappedResponse(status=AppConst.STATUS_PHONE_EXISTED, message="手机号已经存在")

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

def member_logout(request):
    request.session.get()
    pass


@parameter_necessary('phoneNumber', )
@never_cache
@require_POST
def member_resiter_sms_send(request):
    phoneNumber = request.POST.get(modelKey.KEY_PHONENUMBER)
    print('regist phone number %s'%phoneNumber)
    smsType = request.POST.get('smsType')
    if (userhelper.phoneNumberExist(phoneNumber)):
        return JSONWrappedResponse(status=AppConst.STATUS_PHONE_EXISTED, message="手机号已经存在")
    url = 'https://api.leancloud.cn/1.1/requestSmsCode'
    values = {
        modelKey.KEY_LEAN_PHONENUMBER: str(phoneNumber),
        "template": "register",
    }
    if smsType == '2':
        values['smsType'] = 'voice'
    else:
        pass
    headers = {'X-LC-Id': APP_ID, 'X-LC-Key': APP_KEY, 'Content-Type': 'application/json'}
    print(values)
    response = requests.post(url, data=json.dumps(values), headers=headers)
    # 使用异步
    # print(response.status_code)
    # print(str(response.content))
    # print(response.request.body)
    if response.status_code == 200:
        return JSONWrappedResponse(status=AppConst.STATUS_SUCCESSS, message='发送验证码成功')
    else:
        response_dic = response.json()
        return JSONWrappedResponse(status=response_dic['code'], message=response_dic['error'])


@never_cache
@api_view(['POST',])
@permission_classes((IsAuthenticated,))
@parser_classes((JSONParser,))
def installationId_register(request, formate=None):
    json = request.data
    print(str(json))
    serializer = InstallationSerializer(data=json)
    if serializer.is_valid():
        print('valid'+serializer.__str__())
        serializer.save()
        return JSONWrappedResponse(status=AppConst.STATUS_SUCCESSS, message="上传成功")
    else:
        print(serializer.errors)
        return JSONWrappedResponse(status=AppConst.STATUS_ERROR, message=str(serializer.errors))


@csrf_exempt
@parameter_necessary('phoneNumber')
def installationId_bind(request):
    phoneNumber = request.POST.get(modelKey.KEY_PHONENUMBER)
    installationId = request.POST.get('installationId')
    deviceToken = request.POST.get('deviceToken')
    if phoneNumber:
        if installationId:
            try:
                installDevice = Installation.objects.get(installationId=installationId)
                user = User.objects.get(phone_number=phoneNumber)
                installDevice.member = user
                installDevice.save()
                return JSONWrappedResponse(status=AppConst.STATUS_SUCCESSS, message="success")
            except Installation.DoesNotExist:
                return JSONWrappedResponse(status=111,message="这个installationId尚未注册到服务端")
            except User.DoesNotExist:
                return JSONWrappedResponse(status=112, message="这个phoneNumber尚未注册到服务端")
        elif deviceToken:
            return JSONWrappedResponse(status=113,message="ios还没写,哇咔咔")


access_key = 'u-ryAwaQeBx9BS5t8OMSPs6P1Ewoqiu6-ZbbMNYm'
secret_key = 'hVXFHO8GusQduMqLeYXZx_C5_c7D-VSwz6AKhjZJ'


@api_view(['GET'])
@parameter_necessary('userId', )
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def get_uploadAvatarToken(request):
    q = Auth(access_key,secret_key)
    bucket_name = 'hotelbook'
    userId = parse_get_userId(request)
    imageName = 'avatar_'+userId+'.jpg'
    key = imageName

    token = q.upload_token(bucket_name, key, 3600)
    return JSONWrappedResponse(data ={'token':token,'imageUrl':key})


def update_user_avatar_callback(request):
    """
    采用 用户发起请求，获取ｔｏｋｅｎ，客户端得到token往　七牛云上传图片，七牛云回调我方接口的调用流程
    这个接口是  在用户上传之后 ，七牛云回调的我方接口
    :param request:
    :return:
    """
    query_params =  request.query＿params
    fname = query_params.get('filename')
    userId = fname.split('-')[0]
    if(User.existUserId(userId)):
        userhelper.updateAvatar(userId,fname)

# -------------------------基于类的视图----------------------------------------------#
from  rest_framework.views import APIView
from  rest_framework.generics import GenericAPIView,ListAPIView
from django.utils.decorators import method_decorator


class HotelView(GenericAPIView):

    @method_decorator(parameter_necessary('id', ))
    def get(self,request):
        print('process hotel')
        query_params = request.query_params
        id = query_params.get('id')
        excludes_str = query_params.get('excludes')

        print('id is{}'.format(id))
        hotel = Hotel.objects.get(id=id)
        hotel_serializer =  HotelSerializer(hotel,many=False)
        return DefaultJsonResponse({'hotel':hotel_serializer.data})


class HotelListView(ListAPIView):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        city_id = request.query_params.get('cityId')
        hotels =queryset.filter(city_id=city_id)
        try:
            page = request.query_params.get('page',1)
            if int(page) < 1 :
                page =1
        except ValueError as e:
            print('catch error'+e.__str__())

        print(hotels)
        pageintor = Paginator(hotels,1)
        try:
            backHotels = pageintor.page(page)
            serializers = self.serializer_class(backHotels,many=True,excludes=('houses',))
        except EmptyPage as e:
            return DefaultJsonResponse(status=-100,message='没有更多数据')

        return DefaultJsonResponse({'hotels':serializers.data})


class ProvinceView(APIView):

    def get(self, request):
        provinces = Province.objects.all()
        serializer_provinces = ProvinceSerializer(provinces, many=True)
        data = {'procinces': serializer_provinces.data,}
        return DefaultJsonResponse(data=data, )


# ----------------------------- NonView Method---------------------------------------
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


def phoneNumberExist(phoneNumber):
    return User.objects.exists(phoneNumber=phoneNumber)


def parse_get_userId(request):
    userId = request.REQUEST.get('userId')
    return userId