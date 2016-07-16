from django.db import models

from hotelBooking.models import BaseModel


class test (BaseModel):
    class Meta:
        app_label = 'hotelBooking'

    test1 = models.CharField()