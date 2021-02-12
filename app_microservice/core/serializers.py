from django.db import models

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from google.cloud import pubsub_v1
import json

from .models import Favorites, Offer, Subscriptions, WSUser
from ..app_microservice.settings import PROJECT_ID, TOPIC_ID


class WSUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WSUser
        fields = [
            'url', 'uuid', 'name', 'email', 'is_staff', 'profileImageName'
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'}
        }


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, data):
        super(OfferSerializer, self).create(data)

        print(data)
        recommend_data = '{"breed": "schaeferhund"}'
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
        recommend_data = recommend_data.encode("utf-8")
        publisher.publish(topic_path, recommend_data)

        print(f"Published messages to {topic_path}.")

    class Meta:
        model = Offer
        fields = [
            'url', 'uuid', 'name', 'age', 'species', 'breed', 'sterile',
            'description', 'date_published', 'published_by'
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'published_by': {'lookup_field': 'uuid'}
        }


class FavoritesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Favorites
        fields = ['url', 'user', 'offer']
        extra_kwargs = {
            'user': {'lookup_field': 'uuid'},
            'offer': {'lookup_field': 'uuid'}
        }


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
