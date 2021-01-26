from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Offer, Favorites

class UserSerializer(serializers.HyperlinkedModelSerializer):

    #offers = serializers.PrimaryKeyRelatedField(many=True, queryset=Offer.objects.all())
    #groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())

    class Meta:
        model = User
        fields = ['url', 'username', 'is_staff', 'email', 'offers']

class OfferSerializer(serializers.HyperlinkedModelSerializer):

    #published_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Offer
        fields = ['url', 'name', 'age', 'species', 'breed', 'sterile', 'description', 'date_published', 'published_by']

class FavoritesSerializer(serializers.HyperlinkedModelSerializer):

    #user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    #offers = serializers.PrimaryKeyRelatedField(queryset=Offer.objects.all())

    class Meta:
        model = Favorites
        fields = ['url', 'user', 'offers']
