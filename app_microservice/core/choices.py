from django.db import models


class SocialLogin(models.TextChoices):
    Google = "google"


class Species(models.TextChoices):
    DOG = 'Dog'
    CAT = 'Cat'
    SHARK = 'Shark'
    DINOSAUR = 'Dinosaur'


class Breed(models.TextChoices):
    JACK_RUSSEL = 'Jack Russel'
    PERSIAN = 'Persian'
    WHITE_SHARK = 'White Shark'
    KAWUK = 'Kawuk'


BREEDS_FOR_SPECIES = {
    Species.DOG: [
        Breed.JACK_RUSSEL,
    ],
    Species.CAT: [
        Breed.PERSIAN,
    ],
    Species.SHARK: [
        Breed.WHITE_SHARK,
    ],
    Species.DINOSAUR: [
        Breed.KAWUK,
    ]
}


class Sex(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'
