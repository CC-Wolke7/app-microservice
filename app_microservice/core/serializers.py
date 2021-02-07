from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Favorites, Offer, WSUser


class WSUserSerializer(serializers.HyperlinkedModelSerializer):

    # offers = serializers.PrimaryKeyRelatedField(many=True, queryset=Offer.objects.all()) # noqa
    # groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all()) # noqa

    class Meta:
        model = WSUser
        fields = [
            'url', "uuid", 'username', 'password', 'is_staff', 'email',
            'offers'
        ]


class OfferSerializer(serializers.HyperlinkedModelSerializer):

    # published_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) # noqa

    class Meta:
        model = Offer
        fields = [
            'url', 'name', 'age', 'species', 'breed', 'sterile', 'description',
            'date_published', 'published_by'
        ]


class FavoritesSerializer(serializers.HyperlinkedModelSerializer):

    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # offers = serializers.PrimaryKeyRelatedField(queryset=Offer.objects.all())

    class Meta:
        model = Favorites
        fields = ['url', 'user', 'offers']


class AuthTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        del token['user_id']
        token['sub'] = str(user.uuid)
        token['name'] = user.username
        token['email'] = user.email

        return token
