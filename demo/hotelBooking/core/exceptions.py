from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
class ConditionDenied(Exception):
    default_detail = '不满足验证条件'
    def __init__(self, detail):
        if detail is not None:
            self.detail = force_text(detail)
        else:
            self.detail = force_text(self.default_detail)

class PointNotEnough(ConditionDenied):
    default_detail = _('积分不够.')

    def __init__(self, method, detail=None):
        if detail is not None:
            self.detail = force_text(detail)
        else:
            self.detail = force_text(self.default_detail).format(method=method)

class PwdSetDenied(ConditionDenied):
    default_detail = _('密码错误')


class UserCheck:
    @staticmethod
    def validate_pwd(value):
        if len(value) < 6:
            raise PwdSetDenied(detail='密码位数太短，应该大于6位')
