from django.db import models
from django.utils.translation import ugettext_lazy as _
class CheckMixin(models.Model):
    checked = models.BooleanField(_('审核过 ?'),default=False,blank=True)
    active= models.BooleanField(_('是否可用 ?'),default=False,blank=True)

    class Meta:
        abstract =True