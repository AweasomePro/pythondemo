from rest_framework.views import exception_handler
from ..helper.AppJsonResponse import DefaultJsonResponse


def custom_exception_handle(exc, context=None):
    """
       Returns the response that should be used for any given exception.

       By default we handle the REST framework `APIException`, and also
       Django's built-in `Http404` and `PermissionDenied` exceptions.

       Any unhandled exceptions may return `None`, which will cause a 500 error
       to be raised.
       """
    response = exception_handler(exc,context)
    if response is not None:
        response_data = response.data
        print(type(response_data))
    return DefaultJsonResponse(code=-100,message=response_data['detail'])