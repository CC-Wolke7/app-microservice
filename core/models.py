from django.contrib.auth.models import User
from django.db import models

class Offer(models.Model):
    name = models.CharField(max_length=60)
    age = models.IntegerField()
    species = models.CharField(max_length=60)
    breed = models.CharField(max_length=60)
    sterile = models.BooleanField()
    description = models.CharField(max_length=60)
    date_published = models.DateField()
    published_by = models.ForeignKey(User, related_name='offers', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['date_published']

class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offers = models.ForeignKey(Offer, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user']
