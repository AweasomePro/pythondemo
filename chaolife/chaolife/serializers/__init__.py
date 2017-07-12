#-*- coding: utf-8 -*-
from .user import CustomerUserSerializer,UpdateMemberSerializer
from .city import CitySerializer
from .hotels import HotelImgSerializer,HotelSerializer,RoomImgSerializer,RoomPackageSerializer,RoomSerializer
from .products import RoomPackageSerializer,RoomDayStateSerializer
from .province import ProvinceSerializer
from .orders import OrderSerializer, HotelOrderSerializer
from .installation import InstallationSerializer
from .splashImg import SplashImgSerializer