import time

from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework_jwt.settings import api_settings

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Favorites, Offer, WSUser
from .permissions import IsAdminOrOwner, IsAdminOrOwnerOrReadOnly
from .serializers import FavoritesSerializer, OfferSerializer, WSUserSerializer


class WSUserViewSet(viewsets.ModelViewSet):
    queryset = WSUser.objects.all().order_by('-date_joined')
    serializer_class = WSUserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True)
    def create_token(self, request, *args, **kwargslf):

        google_token = request.META['HTTP_AUTHORIZATION'][7:]

        #try:
        idinfo = id_token.verify_oauth2_token(google_token, requests.Request(), '882517722597-3p6j1koj84oa27kv4bc9t58egianqf3e.apps.googleusercontent.com')
        userid = idinfo['sub']

        google_user = self.queryset.filter(
            externalId=userid, signUpMethod='google'
        )

        if (not google_user.exists()):
            WSUser.objects.create(
                username=idinfo['name'],
                is_staff=False,
                email=idinfo['email'],
                offers=[],
                externalId=userid,
                signUpMethod='google'
            )

        # uuid = generare_uuid() TODO
        payload = api_settings.JWT_PAYLOAD_HANDLER(idinfo['sub'])
        token = api_settings.JWT_ENCODE_HANDLER(payload)

        return Response(token)
        #except ValueError:
        #    return Response(False)

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.AllowAny]


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [permissions.AllowAny]
