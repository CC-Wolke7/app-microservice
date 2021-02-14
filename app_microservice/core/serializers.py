from google.cloud import pubsub_v1

# from django.conf import settings

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Favorite, Offer, Subscription, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'url', 'uuid', 'name', 'email', 'is_staff', 'profile_image_name'
        ]
        extra_kwargs = {'url': {'lookup_field': 'uuid'}}


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, data):
        print(data)
        recommend_data = '{"breed": "golden_retriever"}'
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(
            #settings.PROJECT_ID, settings.TOPIC_ID
            "wolke-sieben-fs", "newOffer"
        )
        recommend_data = recommend_data.encode("utf-8")
        publisher.publish(topic_path, recommend_data)

        print(f"Published messages to {topic_path}.")
        return super(OfferSerializer, self).create(data)

    class Meta:
        model = Offer
        fields = [
            'url', 'uuid', 'name', 'age', 'species', 'breed', 'sterile',
            'description', 'date_published', 'published_by', 'sex'
        ]
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            },
            'published_by': {
                'lookup_field': 'uuid'
            }
        }


class FavoriteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Favorite
        fields = ['url', 'user', 'offer']
        extra_kwargs = {
            'user': {
                'lookup_field': 'uuid'
            },
            'offer': {
                'lookup_field': 'uuid'
            }
        }


class SubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscription
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
