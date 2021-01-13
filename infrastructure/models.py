from django.db import models

class Offer(models.Model):
    name = models.CharField(max_length=60)
    species = models.CharField(max_length=60)
    breed = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
    date_published = models.DateField()

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=60)
    date_created = models.DateField()
    offers = models.ForeignKey(Offer, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name