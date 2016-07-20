from rest_framework.permissions import BasePermission

from hotelBooking.models import Order,HotelPackageOrder
from hotelBooking.exceptions.order import OrderDoesNotExist


class IsOrderCustomer(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        number = request.POST.get('number',None)
        if number:
            request.number = number
            try:
                order = HotelPackageOrder.objects.get(number=number)

                request.order = order
                print('request user is {}'.format(request.user.name))
                print('order customer is {}'.format(request.order.customer))
                return request.user and request.user == request.order.customer
            except Order.DoesNotExist:
                raise OrderDoesNotExist()

