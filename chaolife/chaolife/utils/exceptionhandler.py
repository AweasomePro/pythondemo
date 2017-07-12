
# -*- coding:utf-8 -*-
from rest_framework.exceptions import AuthenticationFailed

from chaolife.exceptions import ConditionDenied
from chaolife.exceptions import PageInvalidate
from common.exceptions import AdminDenied
from ..utils.AppJsonResponse import DefaultJsonResponse
"""
Provides an APIView class that is the base of all views in REST framework.
"""

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from rest_framework import exceptions, status
from rest_framework.compat import set_rollback
from sms.client.exceptions import VertifySmsNotMatchException
from common.exceptions import appcodes

def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    print(exc)
    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            # data = {'detail': exc.detail}
            data = exc.detail
        code = -100
        if isinstance(exc,AuthenticationFailed):
            code = 401
        set_rollback()
        return DefaultJsonResponse(message=data,code=code, status=200, headers=headers)

    elif isinstance(exc, Http404):
        msg = _('Not found.')
        data = {'detail': six.text_type(msg)}
        set_rollback()
        return DefaultJsonResponse(message=data, code=-100,status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, PermissionDenied):
        msg = _('Permission denied.')
        data = {'detail': six.text_type(msg)}
        set_rollback()
        return DefaultJsonResponse(message=msg, status=status.HTTP_403_FORBIDDEN)

    elif isinstance(exc,ConditionDenied):
        print(exc.detail)
        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}
        print(type(exc))
        print(data)
        return DefaultJsonResponse(message=data.get('detail'), code=exc.code, status=status.HTTP_200_OK,)
    elif isinstance(exc,PageInvalidate): # 客户端请求的页码超出
        return DefaultJsonResponse(message=exc.detail, code=exc.code, status=status.HTTP_200_OK,)
    elif isinstance(exc,VertifySmsNotMatchException):
        return DefaultJsonResponse(message=exc.detail, code= appcodes.SMS_VERIFY_FAILED, status=status.HTTP_200_OK,)
    elif isinstance(exc,AdminDenied):
        return DefaultJsonResponse(message='MDZZ')
    return None


def _app_api_exception_handler(exec,context):
    pass


