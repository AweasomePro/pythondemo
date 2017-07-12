#-*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class Consumption(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    type = models.CharField(max_length=255,verbose_name=_('类型'))
    point = models.SmallIntegerField(verbose_name=_('积分'),help_text=_('积分支出'))
    pass
