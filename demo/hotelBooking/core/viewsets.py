from rest_framework import generics
from rest_framework.viewsets import ViewSetMixin


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