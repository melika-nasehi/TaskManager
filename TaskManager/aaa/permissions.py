from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAdminUser


class IsAdminOrOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        print("1")
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            print("2")

            return True

        if IsAdminUser().has_permission(request, view):
            print("3")

            return True

        # Instance must have an attribute named `owner`.
        #return obj.owner == request.user
        print("4")

        return request.user in obj.users.all() and request.user.is_authenticated

