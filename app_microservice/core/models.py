import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import WSUserManager


class WSUser(PermissionsMixin, AbstractBaseUser):
    name = models.CharField(blank=True, db_index=True, max_length=255)
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid.uuid4)
    email = models.EmailField(unique=True, db_index=True)
    externalId = models.CharField(max_length=60)
    signUpMethod = models.CharField(max_length=60)
    description = models.CharField(max_length=200)

    objects = WSUserManager()

    # These attributes are required for the Django auth builtins
    USERNAME_FIELD = 'uuid'
    REQUIRED_FIELDS = ['name']


class Offer(models.Model):
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid.uuid4)
    name = models.CharField(max_length=60)
    age = models.IntegerField()
    species = models.CharField(max_length=60)
    breed = models.CharField(max_length=60)
    sterile = models.BooleanField()
    description = models.CharField(max_length=200)
    date_published = models.DateField()
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
