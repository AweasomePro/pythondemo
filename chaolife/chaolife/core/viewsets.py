from rest_framework import generics
from rest_framework.viewsets import ViewSetMixin

class WithCustomJsonViewSetMixin(object):
    def get_page_meta_data(self):
        return super(WithCustomJsonViewSetMixin,self).get_page_meta_data()

    def get_paginated_data(self, data):
        meta = super(WithCustomJsonViewSetMixin,self).get_page_metadata()
        if 'meta' in data:
            data['meta'].update(meta)
        else:
            data['meta'] = meta
        return data


class GenericJsonViewSet(ViewSetMixin, generics.GenericAPIView):
    """
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    """

    def get_paginated_json_response(self,key, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_painator_json_response(key,data)