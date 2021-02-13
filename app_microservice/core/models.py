import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .choices import Species, Breed, Sex
from .managers import WSUserManager


class WSUser(PermissionsMixin, AbstractBaseUser):
    name = models.CharField(blank=True, db_index=True, max_length=255)
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid.uuid4)
    email = models.EmailField(unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    externalId = models.CharField(max_length=255)
    signUpMethod = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    profileImageName = models.CharField(max_length=255)

    objects = WSUserManager()

    # These attributes are required for the Django auth builtins
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


class Offer(models.Model):
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    species = models.CharField(max_length=255, choices=Species.choices)
    breed = models.CharField(max_length=255, choices=Breed.choices)
    sex = models.CharField(max_length=255, choices=Sex.choices)
    sterile = models.BooleanField()
    description = models.CharField(max_length=255)
    date_published = models.DateField()
    place = models.CharField(max_length=255)
    published_by = models.ForeignKey(WSUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['date_published']


class Favorites(models.Model):
    user = models.ForeignKey(WSUser, on_delete=models.CASCADE)

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)


class Media(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)

    image = models.CharField(max_length=255)


class Subscriptions(models.Model):
    user = models.ForeignKey(WSUser, on_delete=models.CASCADE)

    breed = models.CharField(max_length=255)
