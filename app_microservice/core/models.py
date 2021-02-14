import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .choices import Breed, Sex, SocialLogin, Species
from .managers import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid.uuid4)
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(blank=True, null=True, max_length=255)
    is_staff = models.BooleanField(default=False)
    external_id = models.CharField(max_length=255, db_index=True)
    signup_method = models.CharField(
        max_length=10, db_index=True, choices=SocialLogin.choices
    )
    description = models.CharField(max_length=255, blank=True, null=True)
    profile_image_name = models.CharField(
        max_length=255, blank=True, null=True
    )

    objects = UserManager()

    # These attributes are required for the Django auth builtins
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class Offer(models.Model):
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    species = models.CharField(max_length=255, choices=Species.choices)
    breed = models.CharField(max_length=255, choices=Breed.choices)
    sex = models.CharField(max_length=255, choices=Sex.choices)
    sterile = models.BooleanField()
    description = models.CharField(max_length=255)
    date_published = models.DateField(auto_now=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    published_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date_published']

    def __str__(self):
        return self.name


class OfferImage(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ["offer", "name"]


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "offer"]


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    breed = models.CharField(max_length=255, choices=Breed.choices)

    class Meta:
        unique_together = ["user", "breed"]
