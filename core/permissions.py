from rest_framework import permissions

class IsAdminOrOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a resource or admins to edit it
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the resource or admins
        return obj.published_by == request.user or request.user.is_staff

class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a resource or admins to view it
    """
    def has_object_permission(self, request, view, obj):

        # Write permissions are only allowed to the owner of the resource or admins
        return obj == request.user or request.user.is_staff