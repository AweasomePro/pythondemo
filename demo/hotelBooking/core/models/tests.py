from django.db import models

from hotelBooking.core.models import BaseModel


class test (BaseModel):
    class Meta:
        app_label = 'hotelBooking'

    test1 = models.CharField()