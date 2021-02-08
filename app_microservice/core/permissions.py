from rest_framework import permissions


class OfferPermission(permissions.BasePermission):
    """
    Custom permission to only allow creators of an offer or admins to edit it
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the resource or admins # noqa
        return obj.published_by == request.user or request.user.is_staff


class WSUserPermission(permissions.BasePermission):
    """
    Custom permission to only allow admins or the user itself to view a user-entry
    """
    def has_object_permission(self, request, view, obj):

        # Write permissions are only allowed to the owner of the resource or admins # noqa
        return obj == request.user or request.user.is_staff

class FavoritesPermission(permissions.BasePermission):
    """
    Custom permission to only allow admins or the user itself to view a favorite-entry
    """
    def has_object_permission(self, request, view, obj):

        # Write permissions are only allowed to the owner of the resource or admins # noqa
        return obj == request.user or request.user.is_staff
