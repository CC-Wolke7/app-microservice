from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Favorites, Offer, Subscriptions, WSUser


class WSUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WSUser
        fields = [
            'url', 'uuid', 'name', 'email', 'offers', 'favorites',
            'subscriptions'
        ]
        extra_kwargs = {'url': {'lookup_field': 'uuid'}}


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Offer
        fields = [
            'url', 'uuid', 'name', 'age', 'species', 'breed', 'sterile',
            'description', 'date_published', 'published_by', 'media'
        ]
        extra_kwargs = {'published_by': {'lookup_field': 'uuid'}}


class FavoritesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Favorites
        fields = ['url', 'user', 'offers']
        extra_kwargs = {'user': {'lookup_field': 'uuid'}}


class SubscriptionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriptions
        fields = ['url', 'user', 'breed']
        extra_kwargs = {'user': {'lookup_field': 'uuid'}}


class AuthTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['sub'] = str(user.uuid)
        token['name'] = user.name
        token['email'] = user.email

        return token
