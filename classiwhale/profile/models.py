from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    whale = models.OneToOneField('whale.Whale', blank=True, null=True)

