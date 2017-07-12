from rest_framework.permissions import BasePermission


class PayAuthenticatePermission(BasePermission):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        print(request.data)
        return True