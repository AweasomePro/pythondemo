from rest_framework.views import exception_handler

from hotelBooking.core.exceptions import ConditionDenied
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
from rest_framework.response import Response

def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
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

        set_rollback()
        return DefaultJsonResponse(message=data,code=-100, status=exc.status_code, headers=headers)

    elif isinstance(exc, Http404):
        msg = _('Not found.')
        data = {'detail': six.text_type(msg)}

        set_rollback()
        return DefaultJsonResponse(message=data, code=-100,status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, PermissionDenied):
        msg = _('Permission denied.')
        data = {'detail': six.text_type(msg)}

        set_rollback()
        return DefaultJsonResponse(message=data, status=status.HTTP_403_FORBIDDEN)

    # Note: Unhandled exceptions will raise a 500 error.
    elif isinstance(exc, ConditionDenied):
        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}
        return DefaultJsonResponse(message=data, code=exc.code, status=status.HTTP_400_BAD_REQUEST,)
    return None


