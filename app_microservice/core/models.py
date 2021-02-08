import uuid

from django.contrib.auth.models import User
from django.db import models


class WSUser(User):
    uuid = models.UUIDField(unique=True, db_index=True, default=uuid.uuid4)
    externalId = models.CharField(max_length=60)
    signUpMethod = models.CharField(max_length=60)
    description = models.CharField(max_length=200)


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
    user = models.ForeignKey(WSUser, related_name='favorites', on_delete=models.CASCADE)
    offers = models.ForeignKey(Offer, on_delete=models.CASCADE)
