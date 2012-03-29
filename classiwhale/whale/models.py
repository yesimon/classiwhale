from django.db import models

DEFAULT_SPECIES_ID = 1

class WhaleSpecies(models.Model):
    name = models.CharField(default="Baby Whale", unique=True, max_length=50, blank=True, null=True)
    img = models.ImageField(upload_to="img/whale/WhaleSpecies", blank=True, null=True)
    minExp = models.IntegerField(blank=True, null=True)
    evolution = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return self.name

    @staticmethod
    def getDefaultSpecies():
        return WhaleSpecies.objects.get(name="Baby Whale")

class Whale(models.Model):
    name = models.CharField(default="My Whale", max_length=50, blank=True, null=True)
    exp = models.IntegerField(default=0, blank=True, null=True)
    species = models.ForeignKey('whale.WhaleSpecies', default=DEFAULT_SPECIES_ID, blank=True, null=True)
