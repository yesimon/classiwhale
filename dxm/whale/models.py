from django.db import models

class Whale(models.Model):
    name = models.CharField(default="My Whale", max_length=50, blank=True, null=True)
    exp = models.IntegerField(default=0, blank=True, null=True)
    species = models.ForeignKey('whale.WhaleSpecies', blank=True, null=True)            

class WhaleSpecies(models.Model):
    name = models.CharField(default="Baby Whale", max_length=50, blank=True, null=True)
    img = models.ImageField(upload_to="img/whale/WhaleSpecies", blank=True, null=True)
