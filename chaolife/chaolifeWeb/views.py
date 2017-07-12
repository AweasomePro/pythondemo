# -*- coding:utf-8 -*-
from django.shortcuts import render
from rest_framework.decorators import api_view

from common.utils.AppJsonResponse import DefaultJsonResponse
from datetime import datetime
# Create your views here.
def home(request):
    return render(request,'index.html')

def booking_terms(request):
    return render(request,'booking-terms.html')

def user_service_terms(request):
    return render(request,'user-service-terms.html')


@api_view(['GET',])
def time_now(request):
    return DefaultJsonResponse()
