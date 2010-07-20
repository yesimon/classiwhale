from django.db import models
from django.contrib.auth.models import User
from tweed.tweet.models import Status

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    statuses = models.ManyToManyField(Status, blank=True, through='StatusDetails')
    
    def __unicode__(self):
        return u'%s\'s Profile' % (self.user.username)
    
    class Meta:
        ordering = ["user"]

        
class StatusDetails(models.Model):
    user_profile = models.ForeignKey(UserProfile) # should be unique=True
    status = models.ForeignKey(Status) # should be unique=True
    rating = models.IntegerField(blank=True)
    rated_time = models.DateTimeField(auto_now_add=True)
