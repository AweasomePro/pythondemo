#-*-coding:utf-8-*-

import signal
from ..models import User
from ..core.models.city import City
from ..core.models.province import Province
from ..core.models.hotel import Hotel,House
from ..core.models.image import HotelImg,HouseImg
from ..core.models.installation import Installation
from ..core.models.user import CustomerMember
from ..core.models.orders import Order
from ..core.models.products import Product,HousePackage
import requests
import json
import re
from hotelBooking.utils import modelKey
from hotelBooking.utils.decorators import parameter_necessary,method_route,is_authenticated
from hotelBooking.utils.AppJsonResponse import JSONWrappedResponse,DefaultJsonResponse
from hotelBooking import appcodes
from . import User,CustomerMember


from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods, require_POST

from django.utils.decorators import method_decorator
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth.models import AnonymousUser
from django.db.models.signals import post_save

from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.generics import GenericAPIView,ListAPIView
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes,permission_classes,authentication_classes,detail_route,list_route
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from qiniu import Auth
from rest_framework_jwt.settings import api_settings

__all__ = [
    "User",
    "City",
    "Province",
    "Hotel",
    "House",
    "HouseImg",
    "HotelImg",
    "Installation",
    "HousePackage",
    "CustomerMember",
    "Order",
    "DefaultJsonResponse",
    "appcodes"



]