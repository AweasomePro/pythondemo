from django.db import models
from hotelBooking import Hotel,House
from hotelBooking.core.models.hotel import RoomType


class RoomTypeState(models.Model):

    ROOM_STATE_ENOUGH = 1
    ROOM_STATE_FEW = 2
    ROOM_STATE_NO_EMPTY = 3

    ROOM_STATES = (
        (ROOM_STATE_ENOUGH,'room is enough'),
        (ROOM_STATE_FEW,'room is few'),
        (ROOM_STATE_NO_EMPTY,'room has no empty')
    )

    hotel = models.ForeignKey(Hotel)
    roomType = models.ForeignKey(House,to_field='name')
    date = models.DateField(unique=True)
    state = models.IntegerField(choices=ROOM_STATES,default=ROOM_STATE_ENOUGH)