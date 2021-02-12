import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import WSUserManager


class WSUser(PermissionsMixin, AbstractBaseUser):
    name = models.CharField(blank=True, db_index=True, max_length=255)
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid.uuid4)
    email = models.EmailField(unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    externalId = models.CharField(max_length=60)
    signUpMethod = models.CharField(max_length=60)
    description = models.CharField(max_length=200)
    profileImageName = models.CharField(max_length=60)

    objects = WSUserManager()

    # These attributes are required for the Django auth builtins
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


class Offer(models.Model):
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid.uuid4)
    name = models.CharField(max_length=60)
    age = models.IntegerField()
    species = models.CharField(max_length=60)
    breed = models.CharField(max_length=60)
    sex = models.CharField(max_length=1)
    sterile = models.BooleanField()
    description = models.CharField(max_length=200)
    date_published = models.DateField()
    place = models.CharField(max_length=200)
    published_by = models.ForeignKey(
        WSUser, related_name='offers', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['date_published']


class Favorites(models.Model):
    user = models.ForeignKey(
        WSUser, related_name='favorites', on_delete=models.CASCADE
    )

    offers = models.ForeignKey(Offer, on_delete=models.CASCADE)


class Media(models.Model):
    offer = models.ForeignKey(
        Offer, related_name='media', on_delete=models.CASCADE
    )

    image = models.CharField(max_length=60)


class Subscriptions(models.Model):
    user = models.ForeignKey(
        WSUser, related_name='subscriptions', on_delete=models.CASCADE
    )

    breed = models.CharField(max_length=60)
