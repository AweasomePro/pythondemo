from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import PositiveIntegerField
class PositiveFloatField(models.FloatField):
    description = _("Positive float")

    def get_internal_type(self):
        return "PositiveFloatField"

    def formfield(self, **kwargs):
        defaults = {'min_value': 0}
        defaults.update(kwargs)
        return super(PositiveFloatField, self).formfield(**defaults)


class PointField(PositiveIntegerField):
    description = _('積分')
