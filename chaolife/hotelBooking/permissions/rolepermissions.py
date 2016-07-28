from rest_framework.permissions import BasePermission
from hotelBooking.models.orders import Order

# todo 使用全局的配置方式，不然修改不方便
ROLE_CUSTOMER = 1
PARTNER_CUSTOMER = 2
class PartnerPermission(BasePermission):
    """
        A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return  request.user.role ==2 or request.user.is_admin


    def has_object_permission(self, request, view, order):
        """
        Return `True` if permission is granted, `False` otherwise.
        admin is God!
        """
        return order.seller == request.user or request.user.is_admin

class IsHotelPartnerRole(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return not request.user.is_anonymous() and request.user.is_partner_member

class CustomerPermission(BasePermission):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        print('判断是否有权限{}'.format((not request.user.is_anonymous() and request.user.role == 1) or request.user.is_admin))
        return (not request.user.is_anonymous() and request.user.role == 1) or request.user.is_admin

