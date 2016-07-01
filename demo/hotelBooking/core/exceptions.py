from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
class ConditionDenied(Exception):
    pass

class PointNotEnough(ConditionDenied):
    default_detail = _('积分不够.')

    def __init__(self, method, detail=None):
        if detail is not None:
            self.detail = force_text(detail)
        else:
            self.detail = force_text(self.default_detail).format(method=method)