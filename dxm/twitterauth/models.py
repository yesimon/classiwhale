from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from status.models import Status


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    access_token = models.CharField(max_length=255, blank=True, null=True, editable=False)
    screen_name = models.CharField(max_length=30, blank=True, null=True)
    profile_image_url = models.URLField(blank=True, null=True)
#    verified = models.BooleanField(default=False)
    location = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    description = models.CharField(max_length=160, blank=True, null=True)
    ratings = models.ManyToManyField(Status, blank=True, through='Rating')
    training_statuses = models.ManyToManyField(Status, blank=True, null=True, related_name='training')
    active_classifier = models.CharField(max_length=50, blank=True, null=True)
    classifier_version = models.CharField(max_length=30, blank=True, null=True)
    
    def __unicode__(self):
        return "%s's profile" % self.screen_name
    

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
    def appendTo(statuses, prof):
        ratings = Rating.objects.filter(user_profile=prof,
                                        status__in=[s.id for s in statuses])
        rd = dict([(r.status_id, r) for r in ratings])
        for s in statuses:
            try:
                r = rd[s.id]
                s.rating = r.rating
                if r.rating == 1:
                    s.likeClass = ' active'
                    s.dislikeClass = ' inactive'
                if r.rating == -1:
                    s.likeClass = ' inactive'
                    s.dislikeClass = ' active'
            except KeyError:
                continue
    
    
    
