from google.auth.transport import requests
from google.cloud import storage
from google.oauth2 import id_token

from django.utils.encoding import smart_text

from rest_framework import exceptions, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.settings import api_settings as jwt_settings

from .models import WSUser, Offer, Favorites, Subscriptions
from .permissions import (  # noqa
    WSUserPermission, OfferPermission, FavoritesPermission
)
from .serializers import (
    WSUserSerializer, OfferSerializer, FavoritesSerializer, SubscriptionsSerializer, AuthTokenSerializer
)


class Images(APIView):
    def get(self, request, format=None):
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket('wolkesiebenbucket')
            blob = bucket.blob(request.query_params['name'])
            image = blob.download_as_text()

            return Response(image, status=status.HTTP_200_OK)
        except:  # noqa
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket('wolkesiebenbucket')
            blob = bucket.blob(request.data['name'])
            blob.upload_from_string(request.data['image'])

            return Response(status=status.HTTP_200_OK)
        except:  # noqa
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GoogleIdTokenLoginView(APIView):
    """
    Receives a Google ID token passed as a `Bearer` token in
    the `Authorization` header.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get_jwt_value(self, request):
        auth = request.META.get(jwt_settings.AUTH_HEADER_NAME)

        if not auth:
            return None

        auth = auth.split()
        auth_header_prefix = jwt_settings.AUTH_HEADER_TYPES.lower()

        if len(auth) == 0:
            return None

        if smart_text(auth[0].lower()) != auth_header_prefix.lower():
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed(
                code='invalid_auth_header',
                detail='Invalid Authorization header. No credentials provided'
            )
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed(
                code='invalid_auth_header',
                detail='Invalid Authorization header. Credentials string '
                'should not contain spaces.'
            )

        return smart_text(auth[1])

    def get(self, request, *args, **kwargs):
        google_id_token = self.get_jwt_value(request)

        if google_id_token is None:
            raise exceptions.NotAuthenticated()

        try:
            google_id = id_token.verify_oauth2_token(
                google_id_token,
                requests.Request(),
                '481332583913-cieg25daahj0ujclj002o0ei5der0rsi.apps.googleusercontent.com'  # noqa
            )

            # google_id = {
            #    "sub": "123",
            #    "name": "nik sauer",
            #    "email": "nik.sauer@me.com"
            # }
        except:  # noqa
            raise exceptions.NotAuthenticated()

        user_id = google_id["sub"]

        try:
            user = WSUser.objects.all().get(
                externalId=user_id, signUpMethod='google'
            )
        except WSUser.DoesNotExist:
            name = google_id.get("name")
            email = google_id.get("email")

            if not name or not email:
                raise exceptions.AuthenticationFailed(
                    code='invalid_google_id_claims',
                    detail='Name and email are required Google ID claims.'
                )

            user = WSUser.objects.create(
                name=name,
                email=email,
                externalId=user_id,
                signUpMethod='google'
            )

        token_refresh = AuthTokenSerializer.get_token(user)

        return Response({
            'refresh': str(token_refresh),
            'access': str(token_refresh.access_token)
        })


class WSUserViewSet(mixins.ListModelMixin,
    mixins.CreateModelMixin, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = WSUser.objects.all()
    serializer_class = WSUserSerializer
    permission_classes = [WSUserPermission]
    lookup_field = 'uuid'

    @action(detail=True)
    def get_subscriptions(self, request, *args, **kwargs):
        try:
            subscriber = self.get_object()
            subscriptions = Subscriptions.objects.filter(user=subscriber)

            result = []
            for subscription in subscriptions:
                result.append(subscription.breed)

            return Response(result, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Breeds(APIView):
    def get(self, request, format=None):
        try:
            subscribtion = request.query_params['breed']
            subscribers = Subscriptions.objects.filter(breed=subscribtion)

            result = []
            for subscriber in subscribers:
                result.append(subscriber.user.uuid)

            return Response(result, status=status.HTTP_200_OK)
        except:  # noqa
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [OfferPermission]


class FavoritesViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [FavoritesPermission]

class SubscriptionsViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer
    permission_classes = [FavoritesPermission]
