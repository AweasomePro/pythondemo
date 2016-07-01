from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    invalid_page_message = '非法的page请求参数'

    page_size = 1
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

    def get_painator_json_response(self, data_key, data):
        return DefaultJsonResponse(res_data={data_key:data})
