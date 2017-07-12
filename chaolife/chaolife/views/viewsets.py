# -*- coding:utf-8 -*-
from chaolife.pagination import StandardResultsSetPagination

class CustomSupportMixin(object):
    pagination_class = StandardResultsSetPagination
