from rest_framework.response import Response

from hotelBooking.core.utils.serializer_helpers import wrapper_response_dict
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict

class StandardResultsSetPagination(PageNumberPagination):
    invalid_page_message = '非法的page请求参数'

    page_size = 1
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

    def get_painator_json_response(self, data_key, data):
        return DefaultJsonResponse(res_data={data_key:data})

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('result', data),
            ('code',100)
        ]))