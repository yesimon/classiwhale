from django.db import models
from status.models import Status
from twitterauth.models import UserProfile

# Create your models here.

class StreamDiff(models.Model):
    user_profile = models.ForeignKey(UserProfile, blank=False, null=False)
    status = models.ForeignKey(Status, blank=False, null=False)
    diff = models.BooleanField(blank=False, null=False) # True -> add tweet
    score = models.DecimalField(decimal_places=8, max_digits=10,
        blank=False, null=False)
    algorithm = models.CharField(blank=False, null=False, max_length=200)
    filter_time = models.DateTimeField(auto_now_add=True)

