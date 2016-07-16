from django.core.management.base import BaseCommand, CommandError
from django.db import models
# from placeholders import *
import os
from hotelBooking import Province,City,Hotel,Room,RoomPackage


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('开始')
        zhejiang_pv = Province.objects.create(
           name = '浙江',
           name_py = 'ZheJiang'
        )
        zhejiang_pv.save()
        city_hz = City.objects.create(
            code  = 101,
            name = '杭州',
            name_py = 'HangZhou',
            province = zhejiang_pv
        )
        city_hz.save()

