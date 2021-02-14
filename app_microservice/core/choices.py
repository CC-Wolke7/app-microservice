from django.db import models


class SocialLogin(models.TextChoices):
    Google = "google"


class Species(models.TextChoices):
    DOG = 'Dog'
    CAT = 'Cat'
    SHARK = 'Shark'
    DINOSAUR = 'Dinosaur'
    BIRD = "Bird"
    SPIDER = "Spider"


class Breed(models.TextChoices):
    JACK_RUSSEL = 'Jack Russel'
    PERSIAN = 'Persian'
    WHITE_SHARK = 'White Shark'
    KAWUK = 'Kawuk'
    CHICKEN = "Chicken"
    LION = "Lion"
    BLACK_WIDOW = "Black Widow"
    OWL = "Owl"
    DOMESTIC_CAT = "Domestic Cat"
    WOLF = "Wolf"
    MALTESER = "Malteser"
    ENGLISH_COCKER_SPANIEL = "English Cocker Spaniel"


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
