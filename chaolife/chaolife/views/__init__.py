# -*- coding:utf-8 -*-

from chaolife import appcodes
from chaolife.core.utils.serializer_helpers import wrapper_response_dict
from chaolife.models.image import HotelImg,RoomImg
from rest_framework import views
from rest_framework import viewsets


__all__ = [
    "User",
    "City",
    "Province",
    "Hotel",
    "Room",
    "RoomImg",
    "HotelImg",
    "Installation",
    "RoomPackage",
    "CustomerMember",
    "Order",
    "DefaultJsonResponse",
    "appcodes",
    "views",
    "viewsets",
]