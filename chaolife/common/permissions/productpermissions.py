from rest_framework.permissions import BasePermission


class IsProductOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return request.user == obj.owner
