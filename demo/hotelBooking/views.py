from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
# from rest_framework.renderers import JSONRenderer
from .helper.AppJsonResponse import JSONWrappedResponse
from .models import Member
from .serializers import MemberSerializer
from .helper import userhelper
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

APP_ID = "P0fN7ArvLMtcgsACRwhOupHj-gzGzoHsz"
APP_KEY = "cWK8NHllNg7N6huHiKA1HeRG"
def register(request):
    return


@api_view(['POST'])
def member_login(request):
    phoneNumber = request.POST.get('phoneNumber')
    password = request.POST.get('password')
    try:
        m = Member.objects.get(phoneNumber=phoneNumber, password=password)
        if (not m is None):
            serializer = MemberSerializer(m)
        return JSONWrappedResponse(status=1, message="登入成功")
    except Member.DoesNotExist:
        return JSONWrappedResponse(status=2, message="账号密码错误")


@csrf_exempt
def member_register(request):
    phoneNumber = request.POST.get('phoneNumber')
    password = request.POST.get('password')
    if (not userhelper.phoneNumberisExist(phoneNumber)):
        m = Member()
        m.phoneNumber = phoneNumber
        m.password = password
        m.username = phoneNumber
        m.save()
        serailizer_member = MemberSerializer(m, many=False)
        print(serailizer_member)
        serailizer_member.data
        return JSONWrappedResponse(serailizer_member.data)
    else:
        return JSONWrappedResponse(status=2, message="手机号已经存在")


def send_register_sms(request):
    phoneNumber = request.GET.get('phoneNumber')
    if (not userhelper.phoneNumberisExist(phoneNumber)):
        pass
    else:
        return JSONWrappedResponse(status=2, message="手机号已经存在")
