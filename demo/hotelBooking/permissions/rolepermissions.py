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
        return request.user and request.user.is_partner_member