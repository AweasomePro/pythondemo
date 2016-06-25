from rest_framework.pagination import PageNumberPagination
class StandardResultsSetPagination(PageNumberPagination):
    invalid_page_message = '非法的page请求参数'

    page_size = 1
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100