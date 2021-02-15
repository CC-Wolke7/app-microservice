from django.utils.encoding import smart_str

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from app_microservice import settings


class UserPermission(permissions.BasePermission):
    """
    Custom permission to only allow admins or the user itself to
    view a user-entry
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the resource or admins # noqa
        return str(obj) == str(request.user) or request.user.is_staff


class OfferPermission(permissions.BasePermission):
    """
    Custom permission to only allow creators of an offer
    or admins to edit it
    """
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the resource or admins # noqa
        return str(obj.published_by) == str(request.user) or request.user.is_staff


class FavoritePermission(permissions.BasePermission):
    """
    Custom permission to only allow admins or the user itself to view
    a favorite-entry
    """
    def has_object_permission(self, request, view, obj):

        # Write permissions are only allowed to the owner of the resource or admins # noqa
        return str(obj.user) == str(request.user) or request.user.is_staff


class ServiceAccountTokenReadOnly(permissions.BasePermission):
    """
    The request is authenticated by a valid API Token. It has permission to
    access this resource but the user will still be an AnonymouseUser.

    This is useful for when we need another backend process to access a
    resource in the API.

    Authentication requires a valid `Authorization` header.
    """
    def has_permission(self, request, view):
        auth = request.headers.get("Authorization")
        token = smart_str(auth)

        return all((
            request.method in SAFE_METHODS,
            token in settings.SERVICE_TOKEN_WHITELIST,
        ))


class ServiceAccountTokenReadWrite(permissions.BasePermission):
    """
    The request is authenticated by a valid API Token. It has permission to
    access this resource but the user will still be an AnonymouseUser.

    This is useful for when we need another backend process to access a
    resource in the API.

    Authentication requires a valid `Authentication` header.
    """
    def has_permission(self, request, view):
        auth = request.headers.get("Authentication")
        token = smart_str(auth)

        return token in settings.SERVICE_TOKEN_WHITELIST
