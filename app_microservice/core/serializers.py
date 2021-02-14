import json
from google.cloud import pubsub_v1
from google.auth.credentials import AnonymousCredentials

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.choices import Breed

from .models import Favorite, Offer, Subscription, User

# from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'url', 'uuid', 'name', 'email', 'is_staff', 'profile_image_name'
        ]
        read_only_fields = ['uuid', "is_staff", "profile_image_name"]
        extra_kwargs = {'url': {'lookup_field': 'uuid'}}


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, data):

        recommend_data = json.dumps({"breed": data.breed, "offerUrl": "test"})

        publisher = pubsub_v1.PublisherClient(credentials={})

        topic_path = publisher.topic_path(
            # settings.PROJECT_ID, settings.TOPIC_ID
            "wolke-sieben-fs",
            "newOffer"
        )
        recommend_data = recommend_data.encode("utf-8")
        future = publisher.publish(topic_path, recommend_data)
        print(future.result())

        print(f"Published messages to {topic_path}.")
        return super().create(data)


    class Meta:
        model = Offer
        fields = [
            'url', 'uuid', 'name', 'age', 'species', 'breed', 'sex', 'sterile',
            'description', 'date_published', 'location', 'published_by'
        ]
        read_only_fields = ['uuid', "date_published"]
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


class CreateFavoriteSerializer(serializers.Serializer):
    offer = serializers.SlugRelatedField(
        slug_field='uuid', queryset=Offer.objects.all()
    )


class UploadImageSerializer(serializers.Serializer):
    image = serializers.CharField()


class SubscribeSerializer(serializers.Serializer):
    breed = serializers.ChoiceField(Breed.choices)


class SubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscription
        fields = ['url', 'user', 'breed']
        extra_kwargs = {'user': {'lookup_field': 'uuid'}}


class UploadOfferImageSerializer(serializers.Serializer):
    image = serializers.CharField()
    name = serializers.CharField(max_length=255)


class AuthTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['sub'] = str(user.uuid)
        token['name'] = user.name
        token['email'] = user.email

        return token
