from django.db import models

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

class Sex(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'