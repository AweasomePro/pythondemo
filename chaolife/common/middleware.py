from django.contrib.auth.models import AnonymousUser


class MobilePlatform(object):
    validate_platform = ('android','ios',)


class MobileAppMiddleware(object):
    def process_request(self, request):
        print(request.META.get('HTTP_MOBILE_PLATFORM'))
        self._parse_client_type(request)
        self._parse_platform(request)

    def _parse_platform(self,request):
        request.platform = request.META.get('HTTP_MOBILE_PLATFORM','unknow')

    def _parse_client_type(self,request):
        request.client_type = request.META.get('HTTP_CLIENT_TYPE', 'unknow')
