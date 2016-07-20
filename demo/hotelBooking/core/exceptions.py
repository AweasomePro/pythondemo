from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

from hotelBooking.utils.phoneUtil import phone_is_legal


class ConditionDenied(Exception):
    default_detail = '不满足验证条件'
    def __init__(self, detail=None,code = -100):
        self.code = code
        if detail is not None:
            self.detail = force_text(detail)
        else:
            self.detail = force_text(self.default_detail)

class PointNotEnough(ConditionDenied):
    default_detail = _('积分不够.')


class PwdSetDenied(ConditionDenied):
    default_detail = _('密码错误')

class UserCreateDenied(ConditionDenied):
    default_detail = _('账号非法')

class UserCheck:
    @staticmethod
    def validate_pwd(value):
        if len(value) < 6:
            raise PwdSetDenied(detail='密码位数太短，应该大于6位')

    @staticmethod
    def validate_phoneNumber(value):
        if (not phone_is_legal(value)):
            raise UserCreateDenied(detail='不是合法的手机号')
