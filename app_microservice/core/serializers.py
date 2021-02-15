# import json

# from django.conf import settings

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.choices import BREEDS_FOR_SPECIES, Breed

from .models import Favorite, Offer, Subscription, User

# from google.auth.credentials import AnonymousCredentials
# from google.cloud import pubsub_v1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid', 'name', 'email', 'profile_image_name']
        read_only_fields = ['uuid', 'profile_image_name']


class OfferSerializer(serializers.ModelSerializer):
    published_by = serializers.SlugRelatedField(
        slug_field='uuid', queryset=User.objects.all()
    )

    class Meta:
        model = Offer
        fields = [
            'uuid', 'name', 'age', 'species', 'breed', 'sex', 'sterile',
            'description', 'date_published', 'location', 'published_by'
        ]
        read_only_fields = ['uuid', 'date_published']

    def validate(self, data):
        species = data['species']
        breed = data['breed']

        allowed_breeds = BREEDS_FOR_SPECIES[species]

        if breed not in allowed_breeds:
            raise serializers.ValidationError(
                f"Breed '{breed}' does not belong to species '{species}'"
            )

        return data

    # def create(self, data):
    #     publisher = pubsub_v1.PublisherClient()

    #     topic_path = publisher.topic_path(
    #         settings.GCP_PROJECT_ID, settings.RECOMMENDER_BOT_TOPIC
    #     )

    #     recommend_data = json.dumps({
    #         "breed": data["breed"],
    #         "offerUrl": "test"
    #     })
    #     recommend_data = recommend_data.encode("utf-8")

    #     try:
    #         future = publisher.publish(topic_path, recommend_data)
    #         future.result()
    #         print(f"Published messages to {topic_path}.")
    #         return super().create(data)
    #     except Exception as e:
    #         print(e)
    #         return e, 500


class FavoriteSerializer(serializers.ModelSerializer):
    offer = serializers.SlugRelatedField(
        slug_field='uuid', queryset=Offer.objects.all()
    )
    user = serializers.SlugRelatedField(
        slug_field='uuid', queryset=User.objects.all()
    )

    class Meta:
        model = Favorite
        fields = ['user', 'offer']


class CreateFavoriteSerializer(serializers.Serializer):
    offer = serializers.SlugRelatedField(
        slug_field='uuid', queryset=Offer.objects.all()
    )


class UploadImageSerializer(serializers.Serializer):
    image = serializers.CharField()


class SubscribeSerializer(serializers.Serializer):
    breed = serializers.ChoiceField(Breed.choices)


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='uuid', queryset=User.objects.all()
    )

    class Meta:
        model = Subscription
        fields = ['user', 'breed']


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
