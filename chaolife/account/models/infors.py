from django.db import models

from common.fiels import PhoneNumberField


class PeopleInfor(models.Model):
    name = models.CharField(max_length=255,verbose_name='姓名',)
    phone_number = PhoneNumberField(max_length=255,verbose_name='手机号',)

    class Meta:
        abstract = True