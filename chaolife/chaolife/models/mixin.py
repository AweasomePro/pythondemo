#-*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from chaolife.exceptions import ConditionDenied
from common import appcodes


def is_checked(func):
    def wrapper():
        func()
    return wrapper()


class CheckMixin(models.Model):
    checked = models.BooleanField(_('审核通过'),default=True,blank=True)
    deleted = models.BooleanField(_('已删除 ?'),default=False,blank=True)
    active= models.BooleanField(_('已上线 ?'),default=False,blank=True)

    def set_active(self,):
        if not self.checked:
            raise ConditionDenied(detail='正在审核中',code=appcodes.CODE_PRODUCT_IS_CHECKING)
        self.active = True


    class Meta:
        abstract =True





class ActiveMixin(models.Model):
    active = models.BooleanField(_('是否可用',),default=True,blank=True)
    modified = models.DateTimeField(_(u"State modified"), auto_now_add=True)
    class Meta:
        abstract = True


class DateStateMixin(models.Model):
    create_at = models.DateTimeField(_(u"Created"), auto_now_add=True)

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    create_at = models.DateTimeField(_(u"Created"), auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True