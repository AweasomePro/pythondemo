#-*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.


def validate_card_type(value):
    if not value is None and value not in ('Visa', 'Master', 'AmEx', 'Diners', 'JCB') :
        raise ValidationError('目前不支持的信用卡类型')


class CreditCardMixin(models.Model):

    CREDIT_CARD_TYPE = ('Visa', 'Master', 'AmEx', 'Diners', 'JCB')

    credit_card_type = models.CharField(max_length=10,validators=[validate_card_type,],blank=True,)
    credit_card_number = models.CharField(max_length=30,blank=True,)
    credit_card_validity_date = models.DateField(max_length=2)

    class Meta:

        abstract = True


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class CreateMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True
