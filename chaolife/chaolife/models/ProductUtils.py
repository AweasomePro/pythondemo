#-*- coding: utf-8 -*-
from datetime import timedelta

from django.utils.timezone import datetime

from django.db import transaction
from chaolife.models import RoomPackage,RoomDayState,Hotel
class RoomPackageCreator(object):

    def createRoomPackage(self, owner, hotel, room, default_point, default_price, breakfast):
        # owner = partner, room = room, hotel = hotel, default_s_point = 20, default_s_price = 130, detail = 'zao'
        try:
            with transaction.atomic():
                roompackage = RoomPackage.objects.create(
                    owner = owner,
                    hotel = hotel,
                    room =room,
                    default_point = default_point,
                    default_front_price = default_price,
                    breakfast = breakfast
                )
                roompackage.save()
                print('创建了roompackage')
                return roompackage
        except Hotel.DoesNotExist as e:
            print('error hotel id')
            raise e

    def createRoomDayState(self):
        pass