# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.
from common.models import CreditCardMixin


class HotelType(models.Model):

    name = models.CharField(max_length=10,verbose_name='类型')

    def __str__(self):
        return self.name





