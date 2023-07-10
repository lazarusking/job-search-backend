from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        print(view)
        return request.user and request.user.is_recruiter

    # def has_object_permission(self, request, view, obj):
    #     # Write permissions are only allowed to the owner of the object.
    #     print(repr(obj),obj == request.user)
    #     return obj.user == request.user

class IsJobOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        print(view)
        return request.user and request.user.is_recruiter

    def has_object_permission(self, request, view, obj):
        print(obj,request.user)
        # Write permissions are only allowed to the owner of the object.
        return obj.recruiter == request.user
