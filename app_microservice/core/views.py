import time

from google.auth.transport import requests
from google.cloud import storage
from google.oauth2 import id_token
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Favorites, Offer, WSUser
from .permissions import IsAdminOrOwner, IsAdminOrOwnerOrReadOnly
from .serializers import FavoritesSerializer, OfferSerializer, WSUserSerializer


class Images(APIView):

    def get(self, request, format=None):

        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket('wolkesiebenbucket')
            blob = bucket.blob(request.data['name'])
            image = blob.download_as_text()

            return Response(image, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):

        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket('wolkesiebenbucket')
            blob = bucket.blob(request.data['name'])
            blob.upload_from_string(request.data['image'])

            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                externalId=userid,
                signUpMethod='google'
            )

        # uuid = generare_uuid() TODO
        refresh = RefreshToken.for_user(WSUser.objects.filter(externalId=userid)[0])
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        return Response(token)
        #except ValueError:
        #    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.AllowAny]

class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [permissions.AllowAny]
