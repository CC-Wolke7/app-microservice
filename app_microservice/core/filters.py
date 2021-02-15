from rest_framework import serializers

from .choices import Breed, Species


class SubscribersQuery(serializers.Serializer):
    breed = serializers.ChoiceField(choices=Breed.choices)


class BreedsQuery(serializers.Serializer):
    species = serializers.ChoiceField(choices=Species.choices, required=False)
