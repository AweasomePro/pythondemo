from django.db import models
from django.utils.translation import ugettext_lazy as _
class CheckMixin(models.Model):
    checked = models.BooleanField(_('审核过 ?'),default=False,blank=True)
    active= models.BooleanField(_('是否可用 ?'),default=False,blank=True)

    class Meta:
        abstract =True

class ActiveMixin(models.Model):
    active = models.BooleanField(_('是否可用',),default=True,blank=True)
    modified = models.DateTimeField(_(u"State modified"), auto_now_add=True)
    class Meta:
        abstract = True


class DateStateMixin(models.Model):
    created = models.DateTimeField(_(u"Created"), auto_now_add=True)

    class Meta:
        abstract = True