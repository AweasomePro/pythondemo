#-*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission

from chaolife.models import Order,HotelPackageOrder
from chaolife.exceptions.order import OrderDoesNotExist


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


class OrderRelevantUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True
