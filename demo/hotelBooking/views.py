from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes

# from rest_framework.renderers import JSONRenderer
from .helper.AppJsonResponse import JSONWrappedResponse
from .models import Member, Installation
from .serializers import MemberSerializer, InstallationSerializer
from .helper import userhelper
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib import auth
from django.contrib.sessions.models import Session, SessionManager
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
import requests
import json
from .helper import modelKey
from .helper.decorators import necessary
import logging

logger = logging.getLogger(__name__)

APP_ID = "P0fN7ArvLMtcgsACRwhOupHj-gzGzoHsz"
APP_KEY = "cWK8NHllNg7N6huHiKA1HeRG"


class appstatus:
    status_success = '100'
    status_error = '-100'
    pwd_error = '102'
    phone_existed = '103'
    phone_not_existed = '104'


@never_cache
@necessary('phoneNumber', 'password', )
def member_login(request):
    phoneNumber = request.POST.get(modelKey.KEY_PHONENUMBER)
    password = request.POST.get('password')
    try:
        m = Member.objects.get(phoneNumber=phoneNumber)
        user = authenticate(phoneNumber=phoneNumber, password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            print('login user ' + str(user.phoneNumber))
            kwargs = {'UserEntity': MemberSerializer(m, many=False).data}
            respose = JSONWrappedResponse(data=kwargs, status=appstatus.status_success, message="登入成功")
            print('settings session cookie name is :' + settings.SESSION_COOKIE_NAME)
        else:
            return JSONWrappedResponse(status=appstatus.pwd_error, message="账号密码错误", )
    except Member.DoesNotExist:
        return JSONWrappedResponse(status=appstatus.phone_not_existed, message="不存在该账号")
    except Exception as e:
        print('exception ' + e.__str__())
        return JSONWrappedResponse(status=401, message="服务器内部请求错误")


@never_cache
@csrf_exempt
@require_POST
def member_register(request):
    phone_number = request.POST.get('phoneNumber')
    password = request.POST.get('password')
    sms_code = request.POST.get('smsCode', None)
    print(sms_code)
    if (not userhelper.phoneNumberExist(phone_number)):
        if sms_code != None:
            verifySuccess, message = verifySmsCode(phone_number, password)
            if (True):
                m = Member()
                print('m 的phoneNumber' + str(m.phoneNumber))
                m.phoneNumber = phone_number
                m.set_password(password)
                m.username = phone_number
                print('m 的username =' + str(m.username))
                m.save()
                serailizer_member = MemberSerializer(m, many=False)
                # serailizer_member.data
                kwargs = {'UserEntity': serailizer_member.data}
                return JSONWrappedResponse(data=kwargs, status=appstatus.status_success, message="注册成功")
            else:
                return JSONWrappedResponse(status=appstatus.pwd_error, message="注册失败，验证码错误")
    else:
        return JSONWrappedResponse(status=appstatus.phone_existed, message="手机号已经存在")


def member_logout(request):
    request.session.get()
    pass


@necessary('phoneNumber',)
@never_cache
@require_POST
def send_regist_sms(request):
    phoneNumber = request.POST.get(modelKey.KEY_PHONENUMBER)
    print('regist phone number %s'%phoneNumber)
    smsType = request.POST.get('smsType')
    if (userhelper.phoneNumberExist(phoneNumber)):
        return JSONWrappedResponse(status=appstatus.phone_existed, message="手机号已经存在")
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
        return JSONWrappedResponse(status=appstatus.status_success, message='发送验证码成功')
    else:
        response_dic = response.json()
        return JSONWrappedResponse(status=response_dic['code'], message=response_dic['error'])


@never_cache
@api_view(['POST'])
@parser_classes((JSONParser,))
def put_installtionId(request, formate=None):
    json = request.data
    serializer = InstallationSerializer(data=json)
    if serializer.is_valid():
        print('valid')
        serializer.save()
        return JSONWrappedResponse(status=appstatus.status_success,message="上传成功")
    else:
        print(serializer.errors)
        return JSONWrappedResponse(status=appstatus.status_error,message=str(serializer.errors))


@necessary('phoneNumber')
def bindUserAndMobilePhone(request):
    phoneNumber = request.POST.get(modelKey.KEY_PHONENUMBER)
    installationId = request.POST.get('installationId')
    deviceToken = request.POST.get('deviceToken')
    if phoneNumber:
        if installationId:

            try:
                installDevice = Installation.objects.get(installationId=installationId)
                member = Member.objects.get(phoneNumber=phoneNumber)
                installDevice.member = member
                installDevice.save()
                return JSONWrappedResponse(status=110, message="success")
            except Installation.DoesNotExist:
                return JSONWrappedResponse(status=111,message="这个installtionId尚未注册到服务端")
        if deviceToken:
            return JSONWrappedResponse(status=112,message="ios还没写")
    else:
        return JSONWrappedResponse(status=110, message="没有手机")


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
    return Member.objects.exists(phoneNumber=phoneNumber)
