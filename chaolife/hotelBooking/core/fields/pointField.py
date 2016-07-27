from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db.models import IntegerField


class PointField(IntegerField):
    description = _("积分")
