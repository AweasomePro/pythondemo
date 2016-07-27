from django.db import models

from hotelBooking.models import BaseModel
from hotelBooking.models import RoomPackage

class TestModel (BaseModel):
    class Meta:
        app_label = 'hotelBooking'
