from google.auth.transport import requests
from google.cloud import storage
from google.oauth2 import id_token

from django.utils.encoding import smart_text

from rest_framework import exceptions, mixins, permissions, status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.settings import api_settings as jwt_settings

from app_microservice import settings

from .models import Favorites, Offer, Subscriptions, WSUser, Media
from .permissions import (  # noqa
    FavoritesPermission, OfferPermission, ServiceAccountTokenReadOnly,
    WSUserPermission
)
from .serializers import (
    AuthTokenSerializer, FavoritesSerializer, OfferSerializer,
    SubscriptionsSerializer, WSUserSerializer
)


def download_image(name):
    storage_client = storage.Client()
    bucket = storage_client.bucket('wolkesiebenbucket')
    blob = bucket.blob(name)
    image = blob.download_as_text()

    return image

def upload_image(name, image):
    storage_client = storage.Client()
    bucket = storage_client.bucket('wolkesiebenbucket')
    blob = bucket.blob(name)
    blob.upload_from_string(image)


#TODO Remove ListModelMixin
class WSUserViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = WSUser.objects.all()
    serializer_class = WSUserSerializer
    permission_classes = [WSUserPermission]
    lookup_field = 'uuid'

    # Offers

    @action(detail=True)
    def get_offers(self, request, *args, **kwargs):
        offers = Offer.objects.filter(published_by=self.get_object())

        result = []
        for offer in offers:
            result.append(offer.uuid)

        return Response(result, status=status.HTTP_200_OK)

    # Favorites

    @action(detail=True)
    def get_favorites(self, request, *args, **kwargs):
        favorites = Favorites.objects.filter(user=self.get_object())

        result = []
        for favorite in favorites:
            result.append(favorite.offer.uuid)

        return Response(result, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def favorite(self, request, *args, **kwargs):
        Favorites.objects.create(
            user = self.get_object(),
            offer = Offer.objects.get(uuid=request.data['offer'])
        )

        return Response(status=status.HTTP_201_CREATED)

    # Profile Image

    @action(detail=True)
    def get_profile_image(self, request, *args, **kwargs):
        result = download_image(self.get_object().profileImageName)

        return Response(result, status=status.HTTP_200_OK)

    @action(detail=True, methods=['PUT'])
    def upload_profile_image(self, request, *args, **kwargs):
        WSUser.objects.filter(uuid=self.get_object().uuid).update(profileImageName = request.data['name'])
        self.get_object().save()
        upload_image(request.data['name'], request.data['image'])

        return Response(status=status.HTTP_201_CREATED)

    # Subscriptions

    @action(detail=True)
    def get_subscriptions(self, request, *args, **kwargs):
        subscriptions = Subscriptions.objects.filter(user=self.get_object())

        result = []
        for subscription in subscriptions:
            result.append(subscription.breed)

        return Response(result, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def subscription(self, request, *args, **kwargs):
        Subscriptions.objects.create(
            user = self.get_object(),
            breed = request.data['breed']
        )

        return Response(status=status.HTTP_201_CREATED)


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [OfferPermission]
    lookup_field = 'uuid'

    # Images

    @action(detail=True)
    def get_images(self, request, *args, **kwargs):
        result = []

        for medium in Media.objects.filter(offer=self.get_object()):
            result.append(download_image(medium.image))

        return Response(result, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def uploade_image(self, request, *args, **kwargs):
        Media.objects.create(
            offer=self.get_object(),
            image=request.data['name']
        )

        upload_image(request.data['name'], request.data['image'])

        return Response(status=status.HTTP_201_CREATED)


class FavoritesViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [FavoritesPermission]
    

class SubscriptionsViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer
    permission_classes = [FavoritesPermission]


class Breeds(APIView):
    permission_classes = [ServiceAccountTokenReadOnly]

    def get(self, request, format=None):
        subscribtion = request.query_params['breed']
        subscribers = Subscriptions.objects.filter(breed=subscribtion)

        result = []

        for subscriber in subscribers:
            result.append(subscriber.user.uuid)

        return Response(result, status=status.HTTP_200_OK)


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
            #google_id = id_token.verify_oauth2_token(
            #    google_id_token,
            #    requests.Request(),
            #    '481332583913-cieg25daahj0ujclj002o0ei5der0rsi.apps.googleusercontent.com'  # noqa
            #)

            google_id = {
               "sub": "123",
               "name": "nik sauer",
               "email": "nik.sauer@me.com"
            }
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
