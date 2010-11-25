from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from status.models import Status


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    access_token = models.CharField(max_length=255, blank=True, null=True, editable=False)
    screen_name = models.CharField(max_length=30, blank=True, null=True)
    profile_image_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=160, blank=True, null=True)
    ratings = models.ManyToManyField(Status, blank=True, through='Rating')

    def __unicode__(self):
        return "%s's profile" % self.user
    

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)



class Rating(models.Model):
    user_profile = models.ForeignKey('twitterauth.UserProfile') 
    status = models.ForeignKey(Status) 
    rating = models.IntegerField(blank=True, null=True)
    rated_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Ratings"
        
    @staticmethod
    def appendTo(statuses, user):
        l = len(statuses)
        for i in range(l):
            try:
                r = Rating.objects.get(status = statuses[i].GetId(), user_profile=user)
                statuses[i].rating = r.rating
                if r.rating == 1:
                    statuses[i].likeClass = ' active'
                    statuses[i].dislikeClass = ' inactive'
                if r.rating == -1:
                    statuses[i].likeClass = ' inactive'
                    statuses[i].dislikeClass = ' active'
            except:
                pass
    
    
    
