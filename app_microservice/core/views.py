import time

from google.oauth2 import id_token
from google.auth.transport import requests

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Favorites, Offer, WSUser
from .permissions import IsAdminOrOwner, IsAdminOrOwnerOrReadOnly
from .serializers import FavoritesSerializer, OfferSerializer, WSUserSerializer


def generate_token(sa_keyfile, sa_email, audience, expiry_length=3600):

    now = int(time.time())

    # build payload
    payload = {
        'iat': now,
        # expires after 'expiry_length' seconds.
        "exp": now + expiry_length,
        # iss must match 'issuer' in the security configuration in your
        # swagger spec (e.g. service account email). It can be any string.
        'iss': sa_email,
        # aud must be either your Endpoints service name, or match the value
        # specified as the 'x-google-audience' in the OpenAPI document.
        'aud': audience,
        # sub and email should match the service account's email address
        'sub': sa_email,
        'email': sa_email
    }

    # sign with keyfile
    signer = google.auth.crypt.RSASigner.from_service_account_file(sa_keyfile)
    jwt = google.auth.jwt.encode(signer, payload)

    return jwt


class WSUserViewSet(viewsets.ModelViewSet):
    queryset = WSUser.objects.all().order_by('-date_joined')
    serializer_class = WSUserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True)
    def create_token(self, request, *args, **kwargslf):

        google_token = request.META['HTTP_AUTHORIZATION'][7:]

        try:
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
            token = generate_token(
                'keyfile_TODO', idinfo['email'], '882517722597-3p6j1koj84oa27kv4bc9t58egianqf3e.apps.googleusercontent.com'
            )

            return Response(token)
        except ValueError:
            return Response(False)

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.AllowAny]


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [permissions.AllowAny]
