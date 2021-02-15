from django.utils.encoding import smart_str

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from app_microservice import settings


class UserOrAdminWriteAuthenticatedRead(permissions.IsAuthenticated):
    """
    Custom permission to only allow admins,
    or the user himself, to edit a user.

    Authenticated users may retrieve users and
    their details but not create new ones.
    """
    def has_object_permission(self, request, view, user):
        # Read permissions are granted to any callee, so
        # we'll always allow GET, HEAD or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the
        # owner of the resource or admins
        return str(user) == str(request.user) or request.user.is_staff


class OfferCreatorOrAdminModifyAuthenticatedCreate(permissions.BasePermission):
    """
    Custom permission to only allow creators of
    an offer, or admins, to edit the offer.

    Unauthenticated users may retrieve offers and
    their details but not create new ones.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return permissions.IsAuthenticated().has_permission(request, view)

    def has_object_permission(self, request, view, offer):
        # Read permissions are granted to any callee, so
        # we'll always allow GET, HEAD or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the
        # owner of the resource or admins
        return (
            str(offer.published_by) == str(request.user)
            or request.user.is_staff
        )


class ServiceAccountTokenReadOnly(permissions.BasePermission):
    """
    The request is authenticated by a valid API Token. It has permission to
    access this resource but the user will still be an AnonymouseUser.

    This is useful for when we need another backend process to access a
    resource in the API.

    Authentication requires a valid `Authorization` header.
    """
    def has_permission(self, request, view):
        auth = request.headers.get('Authorization')
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
        auth = request.headers.get('Authentication')
        token = smart_str(auth)

        return token in settings.SERVICE_TOKEN_WHITELIST
