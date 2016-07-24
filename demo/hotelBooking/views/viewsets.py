from hotelBooking.pagination import StandardResultsSetPagination
class CustomViewSetMixin(object):
    pagination_class = StandardResultsSetPagination
