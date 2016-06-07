from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
# from rest_framework.renderers import JSONRenderer
from .helper.AppJsonResponse import JSONWrappedResponse
from .models import Member
from .serializers import MemberSerializer
from .helper import userhelper
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session, SessionManager, SessionStore
import requests
import json
from .helper import modelKey

APP_ID = "P0fN7ArvLMtcgsACRwhOupHj-gzGzoHsz"
APP_KEY = "cWK8NHllNg7N6huHiKA1HeRG"


@api_view(['POST'])
def member_login(request):
    phoneNumber = request.POST.get(modelKey.KEY_PHONENUMBER)
    password = request.POST.get('password')
    try:
        m = Member.objects.get(phoneNumber=phoneNumber)
        print('是否存在m'+str(m))
        if m.check_password(password):
            request.session['member_id'] = m.id
            respose = JSONWrappedResponse(status=1, message="登入成功")
            respose.set_cookie("session_id","321432341")
            return respose
        else:
            return JSONWrappedResponse(status=2, message="账号密码错误")
    except Member.DoesNotExist:
        return JSONWrappedResponse(status=2, message="不存在该账号")
    except Exception:
        return JSONWrappedResponse(status=401, message="请求错误")


@csrf_exempt
def member_register(request):
    phoneNumber = request.POST.get('phoneNumber')
    password = request.POST.get('password')
    print(password)
    if (not userhelper.phoneNumberisExist(phoneNumber)):
        print('phoneNumber 不存在')
        m = Member()
        m.phoneNumber = phoneNumber
        print('m 的phoneNumber'+str(m.phoneNumber))
        m.set_password(password)
        print(m.password)
        m.username = phoneNumber
        m.save()
        serailizer_member = MemberSerializer(m, many=False)
        print(serailizer_member)
        # serailizer_member.data
        return JSONWrappedResponse(serailizer_member,status=1, message="注册成功")
    else:
        return JSONWrappedResponse(status=2, message="手机号已经存在")


def member_logout(request):
    request.session.get()
    pass

def send_regist_sms(request):
    # url = 'https://api.leancloud.cn/1.1/requestSmsCode'
    # values = {"mobilePhoneNumber": 15726814574}
    # jdata = json.dumps(values)
    # req = urllib.request.Request(url, jdata)
    # print(req.get_method())
    # req.add_header('X-LC-Id', APP_ID)
    # req.add_header('X-LC-Key', APP_KEY)
    # req.add_header('Content-Type', 'application/json')
    phoneNumber = request.POST.get(modelKey.KEY_PHONENUMBER)
    url = 'https://api.leancloud.cn/1.1/requestSmsCode'
    values = {modelKey.KEY_LEAN_PHONENUMBER: str(phoneNumber)}
    headers = {'X-LC-Id': APP_ID, 'X-LC-Key': APP_KEY, 'Content-Type': 'application/json'}
    return JSONWrappedResponse(status=1, message="发送成功")
