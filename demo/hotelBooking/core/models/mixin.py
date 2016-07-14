from django.db import models
from django.utils.translation import ugettext_lazy as _
class CheckMixin(models.Model):
    checked = models.BooleanField(_('审核过 ?'),default=False)
    enabled = models.BooleanField(_('是否可用 ?'),default=False)

    class Meta:
        abstract =True