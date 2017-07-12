#-*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

from chaolife.utils.phoneUtil import phone_is_legal
from common import appcodes


class ConditionDenied(Exception):
    detail = '不满足验证条件'
    code = -100

    is_api_exception = True
    def __init__(self, detail=None,code = None):
        if(code != None):
            self.code = code
        else:
            self.code = ConditionDenied.code
        if detail is not None:
            self.detail = force_text(detail)
        else:
            self.detail = force_text(ConditionDenied.detail)

class AdminDenied(Exception):
    def __init__(self, detail=None,):
        if detail is not None:
            self.detail = force_text(detail)
        else:
            self.detail = force_text(ConditionDenied.detail)

class PointNotEnough(ConditionDenied):
    detail = '积分不足'
    code = appcodes.POINT_NOT_ENOUGH
    pass


class PayPwdError(ConditionDenied):
    detail = '支付密码错误'
    code = appcodes.CODE_PAY_PWD_AUTHENTIC_ERROR


class PermissionDenied(Exception):
    detail = '无该权限'
    code = -100

    def __init__(self, detail=None, code=None):
        if (code != None):
            self.code = code
        if detail is not None:
            self.detail = force_text(detail)
        else:
            self.detail = force_text(self.detail)

class PageInvalidate(Exception):
    detail = '页码超了'
    code = -200
    def __init__(self, detail=None, code=None):
        if (code != None):
            self.code = code
        if detail is not None:
            self.detail = force_text(detail)
        else:
            self.detail = force_text(self.detail)

class SmsCodeCheckFaield(ConditionDenied):
    detail = '验证码验证错误'
    code = appcodes.SMS_VERIFY_FAILED
    def __init__(self):
        self.code = appcodes.SMS_VERIFY_FAILED
        self.detail = '验证码验证错误'

class NotExistUser(ConditionDenied):
    code = 404
    detail = '不存在该账号'
    pass

class ResourceNotExist(ConditionDenied):
    def __init__(self):
        self.code = -404
        self.detail = '资源不存在'

class PwdSetDenied(ConditionDenied):
    detail = _('密码错误')

class UserCreateDenied(ConditionDenied):
    detail = _('账号非法')

class UserCheck:
    @staticmethod
    def validate_pwd(value):
        if len(value) < 6:
            raise PwdSetDenied(detail='密码位数太短，应该大于6位')

    @staticmethod
    def validate_phoneNumber(value):
        if (not phone_is_legal(value)):
            raise UserCreateDenied(detail='不是合法的手机号')

