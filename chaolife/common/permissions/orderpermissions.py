from rest_framework.permissions import BasePermission

from chaolife.models import Order,HotelPackageOrder
from chaolife.exceptions.order import OrderDoesNotExist


class IsOrderCustomer(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
            print('has_permission')
            return request.user

    def has_object_permission(self, request, view, obj):
        print('has_object_permission')
        print(request.user.is_admin)
        print(obj.customer==request.user)
        return obj.customer == request.user or request.user.is_admin


class OrderRelevantUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True
