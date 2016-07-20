from rest_framework.permissions import BasePermission


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
        return  request.user.role ==1 or request.user.is_admin


    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True