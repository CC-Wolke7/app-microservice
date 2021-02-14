import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .choices import Breed, Sex, Species
from .managers import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    name = models.CharField(blank=True, db_index=True, max_length=255)
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid.uuid4)
    email = models.EmailField(unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    external_id = models.CharField(max_length=255)
    signup_method = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    profile_image_name = models.CharField(max_length=255, null=True)

    objects = UserManager()

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
    published_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date_published']

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "offer"]


class Media(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    image = models.CharField(max_length=255)


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    breed = models.CharField(max_length=255, choices=Breed.choices)

    class Meta:
        unique_together = ["user", "breed"]
