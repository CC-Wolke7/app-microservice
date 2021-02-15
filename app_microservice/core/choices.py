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
    # Dog
    JACK_RUSSEL = 'Jack Russel'
    WOLF = "Wolf"
    MALTESER = "Malteser"
    ENGLISH_COCKER_SPANIEL = "English Cocker Spaniel"

    # Cat
    DOMESTIC_CAT = "Domestic Cat"
    PERSIAN = 'Persian'
    LION = "Lion"

    # Shark
    WHITE_SHARK = 'White Shark'

    # Dinosaur
    KAWUK = 'Kawuk'

    # Bird
    CHICKEN = "Chicken"
    OWL = "Owl"

    # Spider
    BLACK_WIDOW = "Black Widow"


BREEDS_FOR_SPECIES = {
    Species.DOG: [
        Breed.JACK_RUSSEL,
        Breed.WOLF,
        Breed.MALTESER,
        Breed.ENGLISH_COCKER_SPANIEL,
    ],
    Species.CAT: [
        Breed.DOMESTIC_CAT,
        Breed.PERSIAN,
        Breed.LION,
    ],
    Species.SHARK: [
        Breed.WHITE_SHARK,
    ],
    Species.DINOSAUR: [
        Breed.KAWUK,
    ],
    Species.BIRD: [
        Breed.CHICKEN,
        Breed.OWL,
    ],
    Species.SPIDER: [
        Breed.BLACK_WIDOW,
    ],
}


class Sex(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'
