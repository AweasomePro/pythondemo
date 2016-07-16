from django.db import transaction
from hotelBooking.models import RoomPackage
class RoomPackageCreator(object):


    def createRoomPackage(self, owner,hotelId,roomId,default_point,default_price,):
        # owner = partner, room = room, hotel = hotel, default_point = 20, default_front_price = 130, detail = 'zao'
        try:
            with transaction.atomic():
                roompackage = RoomPackage.objects.create(
                    owner = owner,
                    hotel = hotelId,
                    room =roomId,
                    default_point = default_point,
                    default_price = default_price,
                )
        except:
            pass


        pass

    def createRoomDayState(self):
        pass