#-*- coding: utf-8 -*-
import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _, ungettext_lazy


class PhoneNumberValidator(object):
    message = _('请输入合法的手机号')
    code = 'invalid'
    def __call__(self, value):
        value = force_text(value)
        if not (self.legal_phone(value)):
            raise ValidationError(self.message,self.code)
        pass

    def legal_phone(self, phone_number):
        phoneprefix = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '150', '151', '152',
                       '153',
                       '156', '157', '158', '159', '170', '183', '182', '185', '186', '188', '189']
        if len(phone_number) != 11:
            return False
        else:
            # 检测是否全部是数字
            if phone_number.isdigit():
                if phone_number[:3] in phoneprefix:
                    return True
                else:
                    return False