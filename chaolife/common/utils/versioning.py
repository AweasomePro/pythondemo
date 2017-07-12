from rest_framework.versioning import BaseVersioning
from django.utils.translation import ugettext_lazy as _
from rest_framework.compat import unicode_http_header
from rest_framework import exceptions
from chaolifeProject import settings
class HttpHeaderVersioning(BaseVersioning):
    invalid_version_message = _('Invalid version in "Api_version" header.')

    def determine_version(self, request, *args, **kwargs):
        version = request.META.get('HTTP_API_VERSION')
        if version == None:
            version = settings.DEFAULT_API_VERSION
        version = unicode_http_header(version)
        if not self.is_allowed_version(version):
            raise exceptions.NotAcceptable(self.invalid_version_message)
        return version