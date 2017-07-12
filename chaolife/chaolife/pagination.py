# -*- coding:utf-8 -*-
from rest_framework.response import Response
from django.core.paginator import Paginator as DjangoPaginator
from django.core.paginator import InvalidPage
from django.utils import six
from chaolife.exceptions import PageInvalidate
from common.utils.AppJsonResponse import DefaultJsonResponse
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict


class StandardResultsSetPagination(PageNumberPagination):
    invalid_page_message = '非法的page请求参数'

    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

    def get_painator_json_response(self, data_key, data):
        return DefaultJsonResponse(data={data_key:data})

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        print('page size is {}'.format(page_size))
        if not page_size:
            return None

        if  request.query_params.get(self.page_size_query_param) =='max':

            return None
        paginator = DjangoPaginator(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        print(page_number)

        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise PageInvalidate()

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        data['count'] =self.page.paginator.count
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('result', data),
            ('code',100)
        ]))

