from google.auth.transport import requests
from google.oauth2 import id_token
import json
from google.cloud import pubsub_v1

from django.conf import settings
from django.db import IntegrityError
from django.utils.encoding import smart_text

from rest_framework import exceptions, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.settings import api_settings as jwt_settings

from .bucket import delete_image, download_image, upload_image
from .choices import BREEDS_FOR_SPECIES, Species
from .models import Favorite, Offer, OfferImage, Subscription, User
from .permissions import (
    OfferCreatorOrAdminModifyAuthenticatedCreate, ServiceAccountTokenReadOnly,
    UserOrAdminWriteAuthenticatedRead
)
from .serializers import (
    AuthTokenSerializer, CreateFavoriteSerializer, OfferSerializer,
    SubscribeSerializer, UploadImageSerializer, UserSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserOrAdminWriteAuthenticatedRead]
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.action in ["favorite", "delete_favorite"]:
            return CreateFavoriteSerializer

        if self.action == "upload_profile_image":
            return UploadImageSerializer

        if self.action in ["subscription", "delete_subscription"]:
            return SubscribeSerializer

        return self.serializer_class

    # Offers
    @action(detail=True)
    def get_offers(self, request, *args, **kwargs):
        offer_uuids = Offer.objects.filter(published_by=self.get_object()
                                           ).values_list("uuid", flat=True)

        return Response(offer_uuids, status=status.HTTP_200_OK)

    # Favorites
    @action(detail=True)
    def get_favorites(self, request, *args, **kwargs):
        offer_uuids = Favorite.objects.filter(
            user=self.get_object()
        ).values_list("offer__uuid", flat=True)

        return Response(offer_uuids, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def favorite(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            offer = Offer.objects.get(uuid=request.data['offer'])
        except Offer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            Favorite.objects.create(user=self.get_object(), offer=offer)
        except IntegrityError:
            # favorite already exists
            return Response(status=status.HTTP_409_CONFLICT)

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['DELETE'])
    def delete_favorite(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            favorite = Favorite.objects.get(
                user=self.get_object(), offer__uuid=request.data['offer']
            )
        except Favorite.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        favorite.delete()

        return Response(status=status.HTTP_200_OK)

    # Profile Image
    @action(detail=True)
    def get_profile_image(self, request, *args, **kwargs):
        user = self.get_object()

        if not user.profile_image_name:
            return Response(status=status.HTTP_404_NOT_FOUND)

        image = download_image(user.profile_image_name)

        return Response(image, status=status.HTTP_200_OK)

    @action(detail=True, methods=['PUT'])
    def upload_profile_image(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.get_object()

        image = request.data['image']
        profile_image_name = f"{str(user.uuid)}_profile_image"

        if user.profile_image_name:
            delete_image(user.profile_image_name)

        upload_image(profile_image_name, image)

        user.profile_image_name = profile_image_name
        user.save()

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['DELETE'])
    def delete_profile_image(self, request, *args, **kwargs):
        user = self.get_object()

        if not user.profile_image_name:
            return Response(status=status.HTTP_404_NOT_FOUND)

        delete_image(user.profile_image_name)

        user.profile_image_name = None
        user.save()

        return Response(status=status.HTTP_200_OK)

    # Subscriptions
    @action(detail=True)
    def get_subscriptions(self, request, *args, **kwargs):
        breeds = Subscription.objects.filter(user=self.get_object()
                                             ).values_list("breed", flat=True)

        return Response(breeds, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def subscription(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            Subscription.objects.create(
                user=self.get_object(), breed=request.data['breed']
            )
        except IntegrityError:
            # subscription already exists
            return Response(status=status.HTTP_409_CONFLICT)

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['DELETE'])
    def delete_subscription(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            subscription = Subscription.objects.get(
                user=self.get_object(), breed=request.data['breed']
            )
        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        subscription.delete()

        return Response(status=status.HTTP_200_OK)


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [OfferCreatorOrAdminModifyAuthenticatedCreate]
    lookup_field = 'uuid'

    def create(self, request, *args, **kwargs):
        recommend_data = json.dumps(
            {"breed": request.data["breed"], "offerUrl": "test"})

        publisher = pubsub_v1.PublisherClient()

        topic_path = publisher.topic_path(
            settings.GCP_PROJECT_ID, "newOffer"
        )
        recommend_data = recommend_data.encode("utf-8")
        try:
            future = publisher.publish(topic_path, recommend_data)
            future.result()
            print(f"Published messages to {topic_path}.")

        except Exception as e:
            print(e)

        return super().create(request)


    def get_serializer_class(self):
        if self.action in ["upload_image", "delete_image"]:
            return UploadImageSerializer

        return self.serializer_class

    # Images
    @action(detail=True)
    def get_images(self, request, *args, **kwargs):
        images = []

        for image in OfferImage.objects.filter(offer=self.get_object()):
            images.append(download_image(image.name))

        return Response(images, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def upload_image(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        offer = self.get_object()
        offer_uuid = str(offer.uuid)

        image = request.data['image']

        image_name = request.data['name']
        stored_image_name = f"{offer_uuid}_offer_image_{image_name}"

        upload_image(stored_image_name, image)

        try:
            OfferImage.objects.create(offer=offer, name=stored_image_name)
        except IntegrityError:
            delete_image(stored_image_name)

            # offer_image already exists
            return Response(status=status.HTTP_409_CONFLICT)

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['DELETE'])
    def delete_image(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        offer = self.get_object()
        offer_uuid = str(offer.uuid)

        image_name = request.data['name']
        stored_image_name = f"{offer_uuid}_offer_image_{image_name}"

        try:
            offer_image = OfferImage.objects.get(
                offer=offer, name=stored_image_name
            )
        except OfferImage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        delete_image(stored_image_name)

        offer_image.delete()

        return Response(status=status.HTTP_200_OK)


class SubscribersView(APIView):
    permission_classes = [ServiceAccountTokenReadOnly]

    def get(self, request, format=None):
        user_uuids = Subscription.objects.filter(
            breed=request.query_params['breed']
        ).values_list("user__uuid", flat=True)

        return Response(user_uuids, status=status.HTTP_200_OK)


class SpeciesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        species = request.query_params['species']
        result = []

        if species == 'all':
            result = Species.values
        else:
            result = BREEDS_FOR_SPECIES[species]

        if not result:
            return Response(status=status.HTTP_404_NOT_FOUND)

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
            google_id = id_token.verify_oauth2_token(
                google_id_token,
                requests.Request(),
                settings.GOOGLE_OAUTH_AUDIENCE,
            )

            # google_id = {
            #    "sub": "3ef9c7a3-1333-44b2-b1ed-40eefa96ccdb",
            #    "name": "nik sauer",
            #    "email": "nik.sauer@mes.com"
            # }
        except:  # noqa
            raise exceptions.NotAuthenticated()

        user_id = google_id["sub"]

        try:
            user = User.objects.all().get(
                external_id=user_id, signup_method='google'
            )
        except User.DoesNotExist:
            name = google_id.get("name")
            email = google_id.get("email")

            if not name or not email:
                raise exceptions.AuthenticationFailed(
                    code='invalid_google_id_claims',
                    detail='Name and email are required Google ID claims.'
                )

            user = User.objects.create(
                name=name,
                email=email,
                external_id=user_id,
                signup_method='google'
            )

        token_refresh = AuthTokenSerializer.get_token(user)

        return Response({
            'refresh': str(token_refresh),
            'access': str(token_refresh.access_token)
        })
