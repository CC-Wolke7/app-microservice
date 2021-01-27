from rest_framework import viewsets, permissions, renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from social_django.utils import psa
import time
import google.auth.crypt
import google.auth.jwt

from .permissions import IsAdminOrOwnerOrReadOnly, IsAdminOrOwner

from .models import WSUser, Offer, Favorites
from .serializers import WSUserSerializer, OfferSerializer, FavoritesSerializer

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
        'aud':  audience,
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
    permission_classes = [IsAdminOrOwner]

    @action(methods='POST', detail=True)
    def create_token(self, request, *args, **kwargslf):

        google_token = request.GET.get('access_token')
        if request.backend.do_auth(google_token):

            google_user = self.queryset.filter(externalId=google_token.sub, signUpMethod='google')

            if(not google_user.exists()):
                WSUser.objects.create(username=google_token.name, is_staff=False, email=google_token.email, offers=[])

            #uuid = generare_uuid()
            token = generate_token(self, '', google_token.email, 'app-microservice')

            return Response(token)
        return Response(False)

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]

class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]
