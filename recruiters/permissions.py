from rest_framework import permissions


class IsRecruiterOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        print(repr(obj), "user object")
        # Write permissions are only allowed to the owner of the object.
        print(obj.recruiter == request.user)
        return obj.recruiter == request.user


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        print(view)
        return request.user and request.user.is_recruiter

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the object.
        print(repr(obj), obj == request.user)
        return obj == request.user


class CanSelectAndApply(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        print(view)
        return request.user and request.user.is_recruiter

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the object.
        print(repr(obj), obj.job.recruiter == request.user)
        return obj.job.recruiter == request.user


class IsJobOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_recruiter

    def has_object_permission(self, request, view, obj):
        print(obj, request.user)
        # Write permissions are only allowed to the owner of the object.
        return obj.recruiter == request.user


class IsNotRecruiter(permissions.BasePermission):
    """
    Custom permission to prevent a recruiter from applying to a job.
    """

    def has_object_permission(self, request, view, obj):
        print(obj, request.user)

        return not request.user.is_recruiter
        return super().has_object_permission(request, view, obj)

    def has_permission(self, request, view):
        return not request.user.is_recruiter


class IsRecruiter(permissions.BasePermission):
    """
    Custom permission to prevent a user from editing recruiter objects.
    """

    def has_object_permission(self, request, view, obj):
        print(obj, request.user)

        return request.user.is_recruiter

    def has_permission(self, request, view):
        return request.user.is_recruiter
